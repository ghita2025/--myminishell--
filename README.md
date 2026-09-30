# Minishell

A small Unix shell written in C as a **42 Network / 1337** project by **gstitou and hfegrach**. It reads commands, parses them into a syntax tree, and executes programs with pipes, redirections, and environment-variable expansion.

## Features

- External commands resolved through `PATH` or an explicit path.
- Built-ins: `echo`, `cd`, `pwd`, `export`, `unset`, `env`, and `exit`.
- Pipelines (`|`), input/output redirection (`<`, `>`, `>>`), and heredocs (`<<`).
- Single and double quotes, environment variables, and `$?`.
- Logical operators (`&&`, `||`), parenthesized subshells, and wildcard expansion.
- Interactive input and history through GNU Readline.

This is a student shell implementing a subset of shell behavior, not a replacement for Bash.

## Build and run

Requirements: Linux, a C compiler, Make, and GNU Readline development files. On Debian/Ubuntu:

```sh
sudo apt install build-essential libreadline-dev
git clone https://github.com/ghita2025/--myminishell--.git minishell
cd minishell
make
./minishell
```

`make clean` removes object files; `make fclean` also removes the executable and bundled library. `make bonus` builds the same executable, including the bonus features.

## Examples

Enter these at the Minishell prompt:

```sh
echo hello | tr a-z A-Z
export PROJECT=minishell
echo "$PROJECT"
echo first > output.txt
echo second >> output.txt
cat < output.txt
false || echo fallback
(echo one && echo two) | wc -l
exit 0
```

## Structure and concepts

| Directory | Purpose |
| --- | --- |
| `include/` | Shared types and function declarations |
| `src/parsing/` | Tokenization, syntax tree construction, and heredocs |
| `src/expansion/` | Parameters, field splitting, wildcards, and quote removal |
| `src/execution/` | Built-ins, environment, processes, pipes, and redirections |
| `src/garbage_collector/` | Tracking and freeing temporary allocations |
| `src/libft/` | Supporting C functions |

The project explores `fork`, `execve`, `waitpid`, file descriptors, `pipe`, `dup2`, signals, parsing, and memory ownership. Standalone built-ins such as `cd` run in the shell process so their changes survive; pipeline commands run in child processes.

## Checks and limitations

```sh
make
python3 tests/smoke.py
```

The smoke script checks 15 cases covering basic commands, pipes, quoting, variables, redirections, heredocs, logical operators, subshells, and exit statuses. These checks passed on Linux using GNU Readline 8.2 headers and the installed Readline 8 shared library. They are focused checks, not exhaustive Bash compatibility or memory-leak tests. Interactive signal behavior and wildcard edge cases were not covered by this script.

Known limitations include a restricted numeric range for `exit` and predictable temporary heredoc paths. Run this educational shell in your own development environment; it has not been hardened for shared or privileged use.

## Small maintenance fixes

- Reject trailing non-numeric characters in `exit` arguments, such as `exit 12abc`.
- Resolve commands containing `/` as paths instead of treating their basename as a built-in.

The original implementation and contributor credits are preserved.
