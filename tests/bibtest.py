


from bibclient.bib_api import HTBibInterface


bquery = HTBibInterface()

js = bquery.get_single_record_json("oclc","45678", full=False)
print json.dumps(js, indent=2)

id_dict = [{"oclc":45678, "lccn":"70628581"}, {"id":"1", "oclc":"45678", "lccn":"70628581"},{"id":"2", "oclc":"45678", "lccn":"70628581"}]
print json.dumps(bquery.get_multi_record_json(id_dict, full=True), indent=4)