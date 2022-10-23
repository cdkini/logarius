import json

import click
import gspread
import pandas as pd

SPREADSHEET_NAME = "logarius"


def get_spreadsheet() -> gspread.Spreadsheet:
    service_account = gspread.service_account()
    return service_account.open(SPREADSHEET_NAME)


def get_worksheet(spreadsheet: gspread.Spreadsheet, category: str) -> gspread.Worksheet:
    try:
        return spreadsheet.worksheet(category)
    except gspread.exceptions.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=category, rows=1000, cols=1000)


def init_dataframe(worksheet: gspread.Worksheet) -> pd.DataFrame:
    return pd.DataFrame(worksheet.get_all_records())


def record_entry(df: pd.DataFrame, worksheet: gspread.Worksheet) -> None:
    if df.empty:
        template_str = "{\n\n}"
    else:
        template = {key: None for key in df.columns}
        template_str = json.dumps(template, indent=4)

    user_input = click.edit(template_str, extension=".json", require_save=False)
    assert user_input is not None
    entry = json.loads(user_input)

    df = df.append(entry, ignore_index=True)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


def run(name: str) -> None:
    spreadsheet = get_spreadsheet()
    worksheet = get_worksheet(spreadsheet=spreadsheet, category=name.lower())
    df = init_dataframe(worksheet)
    record_entry(df=df, worksheet=worksheet)
