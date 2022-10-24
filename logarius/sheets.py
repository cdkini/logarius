import json
from typing import List

import click
import gspread
import pandas as pd

SPREADSHEET_NAME = "logarius"


def list_categories(spreadsheet: gspread.Spreadsheet) -> List[str]:
    return [ws.title for ws in spreadsheet.worksheets()]


def record_new_entry(spreadsheet: gspread.Spreadsheet, category: str) -> None:
    worksheet = _get_worksheet(spreadsheet=spreadsheet, category=category)
    df = _init_dataframe(worksheet)
    _record_entry(df=df, worksheet=worksheet)


def get_spreadsheet() -> gspread.Spreadsheet:
    # Moved generated credential file to ~/.config/gspread/service_account.json
    service_account = gspread.service_account()
    return service_account.open(SPREADSHEET_NAME)


def _get_worksheet(
    spreadsheet: gspread.Spreadsheet, category: str
) -> gspread.Worksheet:
    try:
        return spreadsheet.worksheet(category)
    except gspread.exceptions.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=category, rows=1000, cols=1000)


def _init_dataframe(worksheet: gspread.Worksheet) -> pd.DataFrame:
    return pd.DataFrame(worksheet.get_all_records())


def _record_entry(df: pd.DataFrame, worksheet: gspread.Worksheet) -> None:
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
