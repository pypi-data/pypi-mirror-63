import invoke


@invoke.task
def isort(ctx):
    ctx.run('isort -y -m 3 -lai 2 -tc -sg "alembic/*"')
