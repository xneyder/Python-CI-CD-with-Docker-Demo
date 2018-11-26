import sys
sys.path.append('../../')
sys.path.append('fixtures')
import os
import parse_cisco_pcrf as app
import expected_data
import unittest

class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global data
        #Query the Data
        db=app.get_mysql_connection()
        cursor=db.cursor()
        cursor.execute("TRUNCATE TABLE CISCO_PCRF_CPU")

        filename=os.path.join("fixtures", 
                            "bulk-lab2-oam01-201811201830-CISCO_PCRF_CPU.csv"
                            )
        #Load the Data
        if not app.load_file(filename):
            raise Exception("Could not load data to the table")
        cursor.execute("SELECT * from CISCO_PCRF_CPU")
        data=cursor.fetchall()

    def test_num_records(self):
        """
        Test the number of records
        """
        #Number of records
        self.assertEqual(len(data),129, "Incorrect number of records")

    def test_data_loaded(self):
        """
        Test the data loaded from the file
        """
        #Data matches
        not_loaded=set(expected_data.data)-set(data)
        self.assertEqual(len(not_loaded),0,"Data not loaded {not_loaded}"
                             .format(not_loaded=not_loaded))

    def test_data_no_expected(self):
        """
        Test data not expected
        """
        #Data matches
        not_expected=set(data)-set(expected_data.data)
        self.assertEqual(len(not_expected),0,"Data not expected {not_expected}"
                             .format(not_expected=not_expected))

if __name__ == "__main__":
    data=[]
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
