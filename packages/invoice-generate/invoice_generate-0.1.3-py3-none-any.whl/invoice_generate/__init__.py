import logging
import pathlib

import toml
import click
import pdfkit

from datetime import date
from dateutil import relativedelta, parser

from jinja2 import Environment, PackageLoader, select_autoescape


MONTHS_UK = {
    1: "січня",
    2: "лютого",
    3: "березня",
    4: "квітня",
    5: "травня",
    6: "червня",
    7: "липня",
    8: "серпня",
    9: "вересня",
    10: "жовтня",
    11: "листопада",
    12: "грудня",
}

env = Environment(
    loader=PackageLoader("invoice_generate", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


def read_config():
    try:
        return toml.load(pathlib.Path.home() / ".invoice-generate.toml")
    except FileNotFoundError:
        logging.warning("No .invoice-generate.toml in home directory.")
        return {}


def process_context(context):
    contract_date = parser.parse(context["CONTRACT_DATE"]).date()
    return {
        **context,
        "invoice_number": f'{context["INITIALS"]}_{context["invoice_number"]:>04}',
        "invoice_date": context["invoice_date"].strftime("%d/%m/%Y"),
        "total": context["AMOUNT"] + context["COMMISSION_AMOUNT"],
        "FIRST_AND_LAST_NAME_EN": context["FULL_NAME_EN"].rsplit(maxsplit=1)[0],
        "FIRST_AND_LAST_NAME_UK": context["FULL_NAME_UK"].rsplit(maxsplit=1)[0],
        "CONTRACT_DATE_EN": format_date_en(contract_date),
        "CONTRACT_DATE_UK": format_date_uk(contract_date),
        "start_date_en": format_date_en(context["start_date"]),
        "end_date_en": format_date_en(context["end_date"]),
        "start_date_uk": format_date_uk(context["start_date"]),
        "end_date_uk": format_date_uk(context["end_date"]),
    }


def format_date_en(d: date) -> str:
    return d.strftime("%B %d, %Y")


def format_date_uk(d: date) -> str:
    return f"{d.day:>02} {MONTHS_UK[d.month]} {d.year} р."


def infer_period(d: date) -> (date, date):
    fifteenths = relativedelta.relativedelta(day=15)
    last_day_of_month = relativedelta.relativedelta(day=31)
    one_day = relativedelta.relativedelta(days=1)

    first_of_next_month = d + relativedelta.relativedelta(months=1, day=1)
    first_of_this_month = d + relativedelta.relativedelta(day=1)
    fifteenth_of_this_month = d + fifteenths

    candidates = {
        # Days till first of next moths. If this is the min - we are
        # generating invoice for the first part of next moth, a couple of days before the 1st.
        abs(d - first_of_next_month).days: (
            first_of_next_month,
            first_of_next_month + fifteenths,
        ),
        # Days till of this month, if this is the min - we are generating an
        # invoice for the fist part of this month on the first or a couple of days after the fist.
        abs(d - first_of_this_month).days: (
            first_of_this_month,
            first_of_this_month + fifteenths,
        ),
        # Days till 15th of current month. If this is the min - we are around
        # the middle of the month - so generating invoice for the second half of current month.
        abs(d - fifteenth_of_this_month).days: (
            fifteenth_of_this_month + one_day,
            fifteenth_of_this_month + last_day_of_month,
        ),
    }

    return candidates[min(candidates)]


def get_file_name(full_name: str, invoice_date: date) -> str:
    last_name, first_name, *_ = full_name.split()
    return f"{first_name.capitalize()} {last_name.capitalize()} {invoice_date.strftime('%m.%d.%Y')}.pdf"


@click.command()
@click.argument("num", type=click.INT)
@click.option("-a", "--amount", type=click.FLOAT)
@click.option("-e", "--extra-amount", type=click.FLOAT, default=0)
@click.option("-d", "--invoice-date", type=click.DateTime(formats=["%Y-%m-%d"]), is_flag=False)
def main(num, amount, extra_amount, invoice_date):
    if amount and extra_amount:
        raise RuntimeError(
            "--extra-amount and --amount are mutually exclusive."
        )
    config = read_config()

    invoice_date = invoice_date and invoice_date.date() or date.today()
    start_date, end_date = infer_period(invoice_date)
    context = {
        **config,
        "invoice_date": invoice_date,
        "invoice_number": num,
        "start_date": start_date,
        "end_date": end_date,
        "AMOUNT": amount or config["AMOUNT"] + extra_amount,
    }
    output_file_name = get_file_name(context["FULL_NAME_EN"], invoice_date)

    template = env.get_template("template.tpl")
    pdfkit.from_string(
        template.render(process_context(context)),
        pathlib.Path.cwd() / output_file_name,
        options={"--encoding": "utf8", "--quiet": ""},
    )
    print(f"{output_file_name} created.")
