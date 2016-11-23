# -*- coding: utf-8 -*-

import click

from memex.search import config
from memex.search import index


@click.group()
def search():
    """Manage search index."""


@search.command()
@click.pass_context
def reindex(ctx):
    """
    Reindex all annotations.

    Creates a new search index from the data in PostgreSQL and atomically
    updates the index alias. This requires that the index is aliased already,
    and will raise an error if it is not.
    """

    request = ctx.obj['bootstrap']()

    index.reindex(request.db, request.es, request)


@search.command('update-settings')
@click.pass_context
def update_settings(ctx):
    """
    Attempt to update mappings and settings.

    Attempts to update mappings and index settings. This may fail if the
    pending changes to mappings are not compatible with the current index. In
    this case you will likely need to reindex.
    """

    request = ctx.obj['bootstrap']()

    try:
        config.update_index_settings(request.es)
    except RuntimeError as e:
        raise click.ClickException(e.message)