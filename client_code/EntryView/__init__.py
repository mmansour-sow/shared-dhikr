from ._anvil_designer import EntryViewTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EntryEdit import EntryEdit

class EntryView(EntryViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.

  def edit_entry_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Create a copy of the existing entry from the Data Table 
    entry_copy = dict(self.item)
    # Open an alert displaying the 'EntryEdit' Form
    # set the `self.item` property of the EntryEdit Form to a copy of the entry to be updated
    save_clicked = alert(
      content=EntryEdit(item=entry_copy),
      title="Update Entry",
      large=True,
      buttons=[("Save", True), ("Cancel", False)]
    )
    # Update the entry if the user clicks save
    if save_clicked:
      anvil.server.call('update_entry', self.item, entry_copy)
      # Now refresh the page
      self.refresh_data_bindings()
      self.parent.raise_event('x-edit-entry')

  def delete_entry_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Get the user to confirm if they wish to delete the entry
    # If yes, raise the 'x-delete-entry' event on the parent 
    # (which is the entries_panel on Homepage)
    if confirm(f"Are you sure you want to delete {self.item['name']}?"):
      self.parent.raise_event('x-delete-entry', entry=self.item)

  def label_user_validated_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    self.label_user_validated.text = f"{self.item['validated']} / {self.item['count']} validés"

  def validate_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.text_box_1.text:
      anvil.server.call('update_validated', self.item, self.text_box_1.text)
      self.label_user_validated.text = f"{self.item['validated']} / {self.item['count']} validés"
      self.parent.raise_event('x-validated_button-clicked')
    else:
      pass

  def label_a_faire_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    self.label_a_faire.text = f"""{self.label_a_faire.text}
    {self.item['count']}"""





