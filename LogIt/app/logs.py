from dash import dcc
import dash_bootstrap_components as dbc

from app.style import CARD_STYLE

from app.data import Data

class Logs(Data):

    def __init__(self):
        super().__init__()
        self._cards = None

    @property
    def cards(self):
        #Cards Top page text
        self._cards = [dcc.Markdown('# My Log')]

        for date in self.df.index:
            row = self.df.loc[date]
            self._cards.append(dbc.Container(self.card(date), style = CARD_STYLE))

        return self._cards

    def get_note_markdown(self, date):
        note = self.df.loc[date, 'note']
        #NOTE: should be a better way right ?
        if str(note) == 'nan':
            note = '---'

        #Add first elem in markdown list
        return [dcc.Markdown(f'#### {note}')]

    def get_categories_markdown(self, date):
        categories_text = []
        for category in self.categories:
            if str(self.df.loc[date, category]) == 'nan':
                continue

            categories_text.append(
                dcc.Markdown(f'- {category.title()}: {self.df.loc[date, category]}')
            ) 
        return categories_text       

    def get_metadata_markdown(self, date):
        return [dcc.Markdown(f'###### {date}')]

    def card_body(self, date):
        return dbc.CardBody(
            self.get_note_markdown(date) + self.get_categories_markdown(date) + self.get_metadata_markdown(date)
        )

    def card(self, date):
        return dbc.Card(
            [
                dbc.CardHeader(self.df.loc[date, 'title'].title()),
                self.card_body(date)
            ]
        )    