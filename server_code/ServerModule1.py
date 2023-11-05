import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import random


@anvil.server.callable
def add_entry(entry_dict):
  app_tables.entries.add_row(
    created=datetime.now(),
    **entry_dict,
    validated=0
  )

@anvil.server.callable
def get_entries():
  # Get a list of entries from the Data Table, sorted by 'created' column, in descending order
  return app_tables.entries.search(
    tables.order_by("created", ascending=False)
  )

@anvil.server.callable
def update_entry(entry, entry_dict):
  # check that the entry given is really a row in the ‘entries’ table
  if app_tables.entries.has_row(entry):
    entry_dict['updated'] = datetime.now()
    if entry_dict['count'] >= entry['validated']:
      entry.update(**entry_dict)
    else:
      raise Exception("Count cannot be less than validated count")
  else:
    raise Exception("Entry does not exist")

@anvil.server.callable
def delete_entry(entry):
  # check that the entry being deleted exists in the Data Table
  if app_tables.entries.has_row(entry):
    entry.delete()
  else:
    raise Exception("Entry does not exist")

@anvil.server.callable
def get_total_count():
  return sum([entry['count'] if entry['count'] is not None else 0 
              for entry in app_tables.entries.search()
             ])

@anvil.server.callable
def get_total_validated():
  return sum([entry['validated'] if entry['validated'] is not None else 0 
              for entry in app_tables.entries.search()
             ])

@anvil.server.callable
def get_total_remaining_to_validate():
  return get_total_count() - get_total_validated()

@anvil.server.callable
def update_validated(entry, validated):
  if app_tables.entries.has_row(entry):
    if entry['validated'] + validated <= entry['count']:
      entry['validated'] += validated
      entry['updated'] = datetime.now()
      entry.update()
    else:
      raise Exception("Validated count cannot be greater than total count")
  else:
    raise Exception("Entry does not exist")

@anvil.server.callable
def search_users(query):
  result = app_tables.entries.search()
  if query:
    result = [
      x for x in result
      if query.lower() in x['name'].lower()
    ]
  return result