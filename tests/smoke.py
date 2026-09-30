"""Focused behavior checks. Build minishell first; requires Python 3."""
import pathlib, re, subprocess, tempfile
binary = pathlib.Path(__file__).resolve().parents[1] / 'minishell'

def run(command, cwd):
    result = subprocess.run([str(binary)], input=command+'\n', text=True,
                            capture_output=True, timeout=5, cwd=cwd)
    output = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout)
    output = '\n'.join(line for line in output.splitlines()
                       if not line.startswith('Minishell > ') and line != 'exit')
    return result, output

with tempfile.TemporaryDirectory() as d:
    cases = [
        ('echo hello', 'hello', 0),
        ('echo hello | tr a-z A-Z', 'HELLO', 0),
        ('export TEST=world\necho "$TEST"', 'world', 0),
        ("echo '$HOME'", '$HOME', 0),
        ('false\necho $?', '1', 0),
        ('(echo nested) && echo yes', 'nested\nyes', 0),
        ('false || echo fallback', 'fallback', 0),
        ('echo first > out\necho second >> out\ncat < out', 'first\nsecond', 0),
        ('export TEST=x\nunset TEST\necho "[$TEST]"', '[]', 0),
        ('cd /\npwd', '/', 0),
        ('exit 7', '', 7),
        ('exit 12abc', '', 2),
        ('nosuchcommand', '', 127),
        ('/definitely-missing/echo hello', '', 127),
    ]
    for command, expected, status in cases:
        result, output = run(command, d)
        assert (output, result.returncode) == (expected, status), (command, output, result.stderr, result.returncode)
    result, output = run('cat << END\nheredoc text\nEND', d)
    assert '\nheredoc text' in '\n'+output and result.returncode == 0, (output, result.stderr)
print('PASS: 15 cases covering builtins, quoting, expansion, pipelines, redirects,')
print('heredoc, logical operators, subshells, and exit statuses')
