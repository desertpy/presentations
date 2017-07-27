#!/usr/bin/env python
import click

def add(a, b):
    return float(a) + float(b)

@click.command()
@click.argument('a', nargs=1)
@click.argument('b', nargs=1)
def main(a, b):
    print(add(a, b))

if __name__ == '__main__':
    main()
