from bot.storage import load_json, save_json

class Bank:
    def __init__(self, file_path: str = "data/balances.json"):
        self.file_path = file_path
        self._balances = load_json(self.file_path, {})
    
    def _save(self):
        save_json(self.file_path, self._balances)
    
    def _get_server(self, gid):
        if gid is None:
            raise ValueError("This is a server only feature")

        gid = str(gid)
        return self._balances.setdefault(gid, {})

    def bal(self, uid, gid):
        server = self._get_server(gid)
        uid = str(uid)

        if uid not in server:
            server[uid] = 0
            self._save()

        return int(server[uid])
    
    def can_afford(self, uid, gid, amount):
        if not self.bal(uid, gid) >= amount:
            raise ValueError("You're too broke to afford that.")
    
    def deposit(self, uid, gid, amount):
        if amount < 0:
            raise ValueError("amount must be >= 0")

        server = self._get_server(gid)
        uid = str(uid)

        server[uid] = self.bal(uid, gid) + amount
        self._save()
        return int(server[uid])

    def withdraw(self, uid, gid, amount):
        if amount < 0:
            raise ValueError("amount must be >= 0")

        server = self._get_server(gid)
        uid = str(uid)

        current = self.bal(uid, gid)
        if current < amount:
            raise ValueError("insufficient funds")

        server[uid] = current - amount
        self._save()
        return int(server[uid])
    
    def manage_fund(self, uid, gid, wager, multiplier):
        if not multiplier:
            return self.withdraw(uid, gid, wager)
        else:
            return self.deposit(uid, gid, multiplier * wager)