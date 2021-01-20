from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import List
from urllib.request import Request, urlopen
from urllib.parse import urlparse

import typer
from gazpacho import Soup, get
from rich import print
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
)

app = typer.Typer(name="jeejuh-dl")


def get_links(url: str) -> List[Soup]:
    resp = get(url)
    page = Soup(resp)

    if "download page has expired" in resp:
        print(
            "[red]This download page has expired. Need it reactivated? Please contact beats@jeejuh.com."
        )
        raise typer.Exit()

    links = page.find("a", attrs={"href": "/downloader.php?key1"}, partial=True)

    return links


# https://github.com/willmcgugan/rich/blob/0e8f4747cae99d9ccb2596c966af5737e955a932/examples/downloader.py#L36
def download_content(
    task_id: TaskID, filename: str, url: str, orig_url: str, output: Path
):

    headers = {
        "method": "GET",
        "authority": "www.jeejuh.com",
        "scheme": "https",
        "path": url,
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": orig_url,
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
    }

    req = Request("https://www.jeejuh.com" + url, headers=headers)
    response = urlopen(req)
    progress.update(task_id, total=int(response.info()["Content-length"]))

    folder = filename.split(" - ")[1]
    Path(output / folder).mkdir(parents=True, exist_ok=True)
    dest_file = output / folder / filename

    progress.start_task(task_id)
    with open(dest_file, "wb") as file:
        for data in iter(partial(response.read, 32768), b""):
            file.write(data)
            progress.update(task_id, advance=len(data))


def start_downloads(urls: List[Soup], orig_url: str, output: Path, threads: int):
    with progress:
        with ThreadPoolExecutor(max_workers=threads) as pool:
            for url in urls:
                task_id = progress.add_task("download", filename=url.text, start=False)
                pool.submit(
                    download_content,
                    task_id,
                    url.text,
                    url.attrs["href"],
                    orig_url,
                    output,
                )


def domain_check(value: str):
    parsed = urlparse(value)
    if parsed.hostname not in ["jeejuh.com", "www.jeejuh.com"]:
        raise typer.BadParameter("URL does not point to jeejuh.com or www.jeejuh.com")
    return value


@app.command()
def download(
    url: str = typer.Argument(
        ..., help="URL to jeejuh.com download page", callback=domain_check
    ),
    output: Path = typer.Option(
        ".", exists=True, file_okay=False, writable=True, resolve_path=True
    ),
    threads: int = typer.Option(
        5, "--threads", "-t", help="Max number of concurrent downloads"
    ),
):
    links = get_links(url)
    start_downloads(links, url, output, threads)


if __name__ == "__main__":
    app()