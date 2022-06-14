import sys
import datetime

def validate_input(date_input):
  """Validate that input is of correct format"""
  try:
    datetime.datetime.strptime(date_input, '%Y%m%d')
  except ValueError:
    raise ValueError("Input parameter should be YYYYMMDD")
    sys.exit(1)