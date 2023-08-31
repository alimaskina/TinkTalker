from src.ControllerDir.TelegramController import TelegramController
import click


@click.command()
@click.argument('mode', type=str, default='telegram')
def main(mode: str):
    controller = None
    if mode == 'telegram':
        controller = TelegramController()

    controller.run()


if __name__ == '__main__':
    main()

