from tronapi.exceptions import InvalidTronError, TronError


class TransactionBuilder(object):
    def __init__(self, tron):
        self.tron = tron

    def send_trx(self, to, amount, account):
        """Creates a transaction of transfer.
        If the recipient address does not exist, a corresponding account will be created.

        Parameters:
            to (str): to address
            amount (float): amount
            account (str): from address

        Returns:
            Transaction contract data

        """
        if not self.tron.is_address(to):
            raise InvalidTronError('Invalid recipient address provided')

        if not isinstance(amount, float) and amount <= 0:
            raise InvalidTronError('Invalid amount provided')

        _to = self.tron.to_hex(to)
        _from = self.tron.to_hex(account)

        if _to == _from:
            raise TronError('Cannot transfer TRX to the same account')

        return self.tron.full_node.request('/wallet/createtransaction', {
            'to_address': _to,
            'owner_address': _from,
            'amount': self.tron.to_tron(amount)
        }, 'post')