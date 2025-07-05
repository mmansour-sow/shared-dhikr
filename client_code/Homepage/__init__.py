from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.users
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EntryEdit import EntryEdit

class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    self.refresh_entries()
      # Set an event handler on the RepeatingPanel (our 'entries_panel')
    self.entries_panel.set_event_handler('x-delete-entry', self.delete_entry)
    self.entries_panel.set_event_handler('x-validated_button-clicked', self.label_pris_show)
    self.entries_panel.set_event_handler('x-edit-entry', self.label_pris_show)

  def add_entry_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Initialise an empty dictionary to store the user inputs
    new_entry = {}
    # Open an alert displaying the 'EntryEdit' Form
    save_clicked = alert(
      content=EntryEdit(item=new_entry),
      title="Add Entry",
      large=True,
      buttons=[("Save", True), ("Cancel", False)]
    )
    # If the alert returned 'True', the save button was clicked.
    if save_clicked:
      anvil.server.call('add_entry', new_entry)
      self.refresh_entries()
    
  def refresh_entries(self):
     # Load existing entries from the Data Table, 
     # and display them in the RepeatingPanel
     self.entries_panel.items = anvil.server.call('get_entries')
     self.label_pris_show()

  def delete_entry(self, entry, **event_args):
    # Delete the entry
    anvil.server.call('delete_entry', entry)
    # Refresh entry to remove the deleted entry from the Homepage
    self.refresh_entries()

  def label_pris_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    # self.label_pris.text = anvil.server.call('get_total_count')
    self.label_pris.text = f"""
    Objectif:                  41000
    Total pris:               {anvil.server.call('get_total_count')}
    Restant à valider : {anvil.server.call('get_total_remaining_to_validate')}
    Total validé :           {anvil.server.call('get_total_validated')}
    """

  def search(self, **event_args):
    self.entries_panel.items = anvil.server.call(
      'search_users',
      self.text_box_search.text
    )





