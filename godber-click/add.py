#!/usr/bin/env python
import click

def add(a, b):
    return float(a) + float(b)

@click.command()
@click.argument('a', nargs=1, type=click.FLOAT)
@click.argument('b', nargs=1, type=click.FLOAT)
@click.option('--verbose', '-v', is_flag=True, default=False,
              help="generate verbose output")
def main(a, b, verbose):
    """Docstring thing"""
    if verbose:
        print("a: %s" % a)
        print("b: %s" % b)
    print(add(a, b))

if __name__ == '__main__':
    main()
