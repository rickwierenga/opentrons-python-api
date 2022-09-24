""" Somewhat nicer wrapper around ot_api.runs for health related things """

from ot_api.requestor import get as rget

def get():
  return rget("/health")
