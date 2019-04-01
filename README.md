### Transaction Reporting Tool

This tool can be used to generate the following three reports based on everyday transaction logs.

* **DAILY TRANSACTION REPORT:** Displays total incoming and outgoing amount per day. Buy indicates outgoing amount and a Sell indicates incoming amount.

* **ENTITY RANKING REPORT - INCOMING:** Displays ranking of entities based on incoming amount. 

* **ENTITY RANKING REPORT - OUTGOING:** Displays ranking of entities based on outgoing amount. 

### Input Format:
Input is read from stdin. Each transcation should be separated with a newline. Each fields is then separated by a delimiter ("," / comma by default).
Following fiels are mandatory for correct output:
* field1: entity
* field2: transaction type (Buy/Sell)
* field3: agreed_fx
* field6: settlement date (All the dates should follow same format)
* field7: Number of units brought/sold.
* field8: Price per Unit.

### How to use:
reports.py should be invoked with python3. You can see the formatting of inputs from files under tests/
On *nix, Use the following command to execute from current directory (Glasgow)

python3 reports.py < tests/inp0

Replace "tests/inp0" with your own test file.

Thank You!