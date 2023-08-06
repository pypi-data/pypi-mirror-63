"""CLI - Command Line Interface - Using Click"""
import click


@click.command()
def main():
    click.echo("Hello, World!")
