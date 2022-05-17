from functools import lru_cache

import pywikibot as pywikibot


@lru_cache()
def prep_property(property='P279'):
    enwp = pywikibot.Site('en', 'wikipedia')
    wikidata = enwp.data_repository()
    pid = property
    p_page = pywikibot.PropertyPage(wikidata, pid)
    data = p_page.get()
    d = {field: {k: v for k, v in data[field].items()} for field in list(data) if (type(data[field]) != str)}
    aliases_en = d["aliases"].get("en")
    dd = {
            "id": property,
            "label": d["labels"]["en"],
            "description": d["descriptions"].get("en"),
            "alias": aliases_en[0] if aliases_en else None,
            # "claims":d["claims"]
    }
    return dd

def get_prop_en_or_any(d: dict, prop:str):
    pr = d.get(prop)
    if not pr:
        return None
    en_pr = pr.get("en")
    if en_pr:
        return en_pr
    all_pr = list(pr.values())
    if not all_pr:
        return None
    return all_pr[0]

@lru_cache()
def _prep_entity(entity='Q1132755'):
    enwp = pywikibot.Site('en', 'wikipedia')
    wikidata = enwp.data_repository()
    qid = entity
    page = pywikibot.ItemPage(wikidata, qid)
    data = page.get()
    d = {field: {k: v for k, v in data[field].items()} for field in list(data)}

    claims = d["claims"]
    plain_claims = {claim_name: [claim.toJSON() for claim in claim_list] for claim_name, claim_list in
                    claims.items()}

    dd = {
            "id": qid,
            "label": get_prop_en_or_any(d,"labels"),
            "description": get_prop_en_or_any(d,"descriptions"),
            "alias": get_prop_en_or_any(d,"aliases"),
            "claims":d["claims"],
            "plain_claims": plain_claims
    }
    return dd

def prep_raw_entity(entity='Q1132755'):
    dd = _prep_entity(entity)
    dd.pop("claims")
    dd.pop("plain_claims")
    return dd


@lru_cache()
def prep_entity(entity='Q1132755', do_prep_claims=0):
    do_prep_claims = int(do_prep_claims)

    dd = _prep_entity(entity)
    plain_claims = dd["plain_claims"]
    if do_prep_claims != 0:
        cut_claims = {}
        if do_prep_claims == 1:
            for cl, v in plain_claims.items():
                vals = []
                for vv in v:
                    b_ent: bool = False
                    val = vv['mainsnak']['datavalue']["value"]
                    if type(val) == dict:
                        b_ent = True
                        n_val = val.get("numeric-id")
                        if n_val is None:
                            val = str(val)
                        else:
                            val = "Q" + str(n_val)
                    vals.append(str(val))

                # cut_claims[cl.ljust(8,"_")+prep_prop(cl)["label"]] = vals
                cut_claims[cl] = {"id": cl, "label": prep_property(cl)["label"],
                                  "val_type": "entities" if b_ent else "-", "values": vals}

            ret_claims = {k: v for k, v in cut_claims.items() if v['val_type'] == 'entities'}
        elif do_prep_claims == 2:
            claims = [
                    "P31", # instance_of
                    "P279", # subclass of
                    "P366" # has use
            ]
            for cl in claims:

                v = plain_claims.get(cl)
                if not v:
                    continue
                vals = []
                for vv in v:
                    val = vv['mainsnak']['datavalue']["value"]
                    n_val = val.get("numeric-id")
                    val = "Q" + str(n_val)
                    vals.append(str(val))

                cut_claims[cl] = {"id": cl, "label": prep_property(cl)["label"],"val_type": "entities", "values": vals}
            ret_claims = cut_claims
        else:
            ret_claims = {}
        return dd, ret_claims

# @lru_cache()
# def __prep_entity(entity='Q1132755', do_prep_claims=0):
#     do_prep_claims = int(do_prep_claims)
#     enwp = pywikibot.Site('en', 'wikipedia')
#     wikidata = enwp.data_repository()
#     qid = entity
#     page = pywikibot.ItemPage(wikidata, qid)
#     data = page.get()
#     d = {field: {k: v for k, v in data[field].items()} for field in list(data)}
#
#     aliases_en = d["aliases"].get("en")
#     dd = {
#             "id": qid,
#             "label": get_prop_en_or_any(d,"labels"),
#             "description": get_prop_en_or_any(d,"descriptions"),
#             "alias": get_prop_en_or_any(d,"aliases")
#             # "claims":d["claims"]
#     }
#     if do_prep_claims != 0:
#         claims = d["claims"]
#         plain_claims = {claim_name: [claim.toJSON() for claim in claim_list] for claim_name, claim_list in
#                         claims.items()}
#         cut_claims = {}
#         if do_prep_claims == 1:
#             for cl, v in plain_claims.items():
#                 vals = []
#                 for vv in v:
#                     b_ent: bool = False
#                     val = vv['mainsnak']['datavalue']["value"]
#                     if type(val) == dict:
#                         b_ent = True
#                         n_val = val.get("numeric-id")
#                         if n_val is None:
#                             val = str(val)
#                         else:
#                             val = "Q" + str(n_val)
#                     vals.append(str(val))
#
#                 # cut_claims[cl.ljust(8,"_")+prep_prop(cl)["label"]] = vals
#                 cut_claims[cl] = {"id": cl, "label": prep_property(cl)["label"],
#                                   "val_type": "entities" if b_ent else "-", "values": vals}
#
#             ret_claims = {k: v for k, v in cut_claims.items() if v['val_type'] == 'entities'}
#         elif do_prep_claims == 2:
#             claims = [
#                     "P31", # instance_of
#                     "P279", # subclass of
#                     "P366" # has use
#                       ]
#             for cl in claims:
#
#                 v = plain_claims.get(cl)
#                 if not v:
#                     continue
#                 vals = []
#                 for vv in v:
#                     val = vv['mainsnak']['datavalue']["value"]
#                     n_val = val.get("numeric-id")
#                     val = "Q" + str(n_val)
#                     vals.append(str(val))
#
#                 cut_claims[cl] = {"id": cl, "label": prep_property(cl)["label"],"val_type": "entities", "values": vals}
#             ret_claims = cut_claims
#         else:
#             ret_claims = {}
#         return dd, ret_claims
