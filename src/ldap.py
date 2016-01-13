from ldap3 import Server, Connection,AUTH_SIMPLE, STRATEGY_SYNC,GET_ALL_INFO

class LDAP:
    def __init__(self, user, password,baseObject, host, port=389):
        # server object
        self.server = Server(host,
                port=port,
                get_info=GET_ALL_INFO)
        # connection 
        self.connection = Connection(self.server,
                auto_bind=True,
                client_strategy=STRATEGY_SYNC,
                user=user,
                password=password,
                authentication=AUTH_SIMPLE)
        #baseObject
        self.baseObject=baseObject

    def exists(self,baseObject, user,attributes=['sn']):
        """
        check if a user already exists in the DIT
        return bool
        """
        resp = self.connection.search(self.baseObject,
                '(&(objectclass=inetOrgPerson)(sn='+user+'))',
                attributes=attributes)
        return resp
    
    def add(self, dn, attributes=None):
        """
        add a person to the DIT
        """
        resp = self.connection.add(dn, ['inetOrgPerson'],attributes=attributes)
        #print(self.connection.result)
        return resp

    def delete(self,dn):
        """
        delete a user from the DIT
        """
        resp = self.connection.delete(dn)
        #print(self.connection.result)
        return resp

"""
#TEST
baseObject = "ou=people,dc=honeypot,dc=com"
ldap=  LDAP("cn=admin,dc=honeypot,dc=com","ubuntu","baseObject")
ldap.exists(baseObject,"dupont")
#ldap.add('uid=francois,'+baseObject,{'uid':'francois',
#'cn':'francois njeneza','sn':'njeneza'})

ldap.delete("uid=francois,ou=people,dc=honeypot,dc=com")
"""
