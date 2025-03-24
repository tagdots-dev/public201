import click


# 定义一个主命令组
@click.group()
@click.option('--debug/--no-debug', default=False, help='开启或关闭调试模式')
@click.pass_context
def cli(ctx, debug):
    """这是一个使用 click 库的复杂命令行工具示例。"""
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug


# 定义一个子命令，用于创建资源
@cli.command()
@click.argument('resource_name')
@click.option('--type', type=click.Choice(['file', 'directory']), default='file',
              help='指定要创建的资源类型')
@click.pass_context
def create(ctx, resource_name, type):
    """创建一个资源（文件或目录）。"""
    if ctx.obj['DEBUG']:
        click.echo(f"调试模式: 正在创建 {type} {resource_name}")
    click.echo(f"已创建 {type}: {resource_name}")


# 定义一个子命令，用于删除资源
@cli.command()
@click.argument('resource_name')
@click.option('--force', is_flag=True, help='强制删除，不提示确认')
@click.pass_context
def delete(ctx, resource_name, force):
    """删除一个资源。"""
    if not force:
        confirm = click.confirm(f"你确定要删除 {resource_name} 吗？")
        if not confirm:
            click.echo("删除操作已取消。")
            return
    if ctx.obj['DEBUG']:
        click.echo(f"调试模式: 正在删除 {resource_name}")
    click.echo(f"已删除 {resource_name}")


# 定义一个子命令，用于列出资源
@cli.command()
@click.option('--limit', type=int, default=10, help='限制列出的资源数量')
@click.pass_context
def list(ctx, limit):
    """列出资源。"""
    if ctx.obj['DEBUG']:
        click.echo(f"调试模式: 列出最多 {limit} 个资源")
    for i in range(limit):
        click.echo(f"资源 {i + 1}")


# 定义一个子命令，使用环境变量
@cli.command()
@click.option('--config', envvar='MY_APP_CONFIG', default='default_config',
              help='指定配置文件，可通过环境变量 MY_APP_CONFIG 设置')
@click.pass_context
def configure(ctx, config):
    """配置应用程序。"""
    if ctx.obj['DEBUG']:
        click.echo(f"调试模式: 使用配置文件 {config}")
    click.echo(f"应用程序已配置为使用 {config}")


if __name__ == '__main__':
    cli(obj={})
