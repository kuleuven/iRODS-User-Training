The permission management in iRODS is performed by using Access Control Lists (ACLs). The ACL in iRODS is composed of 'read', 'write' and 'own' acess rights. There is also 'null'/'none' to revoke a given permission.

You can look at the table below to know about the impact of ACL:

| Permission Level  | Read     | Write/Edit | Download/Save | Metadata | Rename  | Move    | Delete  |
|-------------------|----------|------------|---------------|----------|---------|---------|---------|
| read              | &#x2713; |            | &#x2713;      |   View   |         |         |         |
| write             | &#x2713; | &#x2713;   | &#x2713;      |Add/Modify|         |         |         |
| own               | &#x2713; | &#x2713;   | &#x2713;      |Add/Modify| &#x2713;| &#x2713;| &#x2713;|
| null              |          |            |               |          |         |         |         |
