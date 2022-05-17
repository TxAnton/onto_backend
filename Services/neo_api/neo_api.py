import contextlib
import io
import json
import sys
import time
from time import sleep
from typing import List, Dict
from Utils import wikidata_prep as wdp
import neo4j
from neo4j import GraphDatabase


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.BytesIO()
    yield
    sys.stdout = save_stdout


class Neo_api(object):
    def __init__(self, host: str = "localhost", port: int = 7687, user: str = "neo4j", pwd: str = "admin",
                 timeout_sec: float = 7):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.uri = f"bolt://{self.host}:{self.port}"
        self.driver = None
        t = time.time()
        while not self.driver and time.time() - t <= timeout_sec:
            try:
                with nostdout():
                    self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.pwd))
            except:
                sleep(1)
        if not self.driver:
            raise Exception(f"Neo4j connection timed out after {timeout_sec} sec")

    def create_entity(self,data,labels="Thing"):
        if type(labels) != list:
            labels=["labels"]
        q = f'''
        MERGE (v{''.join(":"+label for label in labels)}{{{self.dict_to_neo(data)}}})
        RETURN v
        '''
        res = self.exec(q)
        return res

    def link_entities(self,q_s,q_o, predicate,labels="link"):
        if type(labels) != list:
            labels=["labels"]
        q=f'''
        MERGE (s{{id:{q_s}}})
        MERGE (o{{id:{q_o}}})
        MERGE (s)-[p{''.join(":"+label for label in labels)}{{{self.dict_to_neo(predicate)}}}]-(o)
        return p
        '''
        res = self.exec(q)
        return res

    def create_property_by_id(self,sbj_id:str,p_id:str,obj_id:str):
        sbj_d = wdp.prep_entity(sbj_id)
        obj_d = wdp.prep_entity(obj_id)
        p_obj = wdp.prep_property(p_id)

    def do_nothing(self):
        pass

    @staticmethod
    def dict_to_neo(_dict: dict):
        s = ''
        for k, v in _dict.items():
            if v is not None:
                s += f'{k}:{json.dumps(v, ensure_ascii=False)},'
        return s.strip(',')

    def get_currencies(self):
        q = 'match (n:Currency) return n'
        res = self.exec(q)
        return [dict(i[0]) for i in res]

    def create_vacancy_all(self, vacancy_all: Dict):
        vac_all = vacancy_all
        key_skills: List[str] = vac_all.get("key_skills") or []
        q = f'MERGE (v:Vacancy{{{self.dict_to_neo(vac_all["vacancy"])}}}) ' \
            f'MERGE (v)-[:HAS_TYPE]->(t) '

        try:
            res = self.exec(query=q)
        except:
            res = None
        return res

    def create_search_index_if_not_exest(self):
        exists = str(self.exec("CALL db.indexes")).find("FULLTEXT") != -1
        res = None
        if not exists:
            q = "CALL db.index.fulltext.createNodeIndex('descriptions', ['Vacancy'], ['name','responsibility', 'requirement'], {analyzer: 'russian'})"
            q1 = 'CREATE CONSTRAINT ON (n:Vacancy) ASSERT n.id IS UNIQUE'
            try:
                res = self.exec(q)
            except:
                pass
            try:
                res = self.exec(q1)
            except:
                pass

        return exists

    def hello_world(self):
        message = "hello"
        q = "CREATE (a:Greeting) " \
            f"SET a.message = '{message}' " \
            "RETURN a.message + ', from node ' + id(a)"
        return self.exec(q)

    def exec(self, query: str):
        transaction = lambda tx: tx.run(query).values()

        with self.driver.session() as session:
            return session.write_transaction(transaction)

    def __del__(self):
        self.driver.close()
