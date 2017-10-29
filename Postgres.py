import psycopg2

class Postgress():
	def __init__(self,address):
		self.db=psycopg2.connect(address)
		self.cur=self.db.cursor()

	def __del__(self):
		self.cur.close()
		self.db.close()

	def write(self,user,col,data):
		self.cur.execute(f"""select {col} from users where id = {user}""")
		if self.cur.fetchall():
			self.cur.execute(f"""update users set {col}='{data}' where id = {user}""")
			self.db.commit()
		else:
			self.cur.execute(f"""insert into users (id,{col}) values({user},'{data}')""")
			self.db.commit()

	def read(self,user,col):
		self.cur.execute(f"""select {col} from users where id={user}""")
		data=self.cur.fetchall()[0][0]
		print(data)
		if data:
			if type(data)==type("str"):
				data=data.strip()
			return data
		else:
			return None

if __name__=="__main__":
	pgres=Postgress("postgres://lciehxdy:m2xMdBB_HMr_QrvwntIeGva5ngPcSNL7@dumbo.db.elephantsql.com:5432/lciehxdy")
