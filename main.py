from app.config import load_settings
from app.pages import folder, home, page, search
from app.wiki import WikiStore
from nicegui import ui


def main() -> None:
    settings = load_settings()

    store = WikiStore(settings.wiki_path)
    store.load()

    home.register(store, settings)
    folder.register(store, settings)
    page.register(store, settings)
    search.register(store, settings)

    ui.run(
        title=settings.title,
        host=settings.host,
        port=settings.port,
        reload=False,
        show=False,
        dark=settings.dark_mode,
    )


if __name__ == "__main__":
    main()
