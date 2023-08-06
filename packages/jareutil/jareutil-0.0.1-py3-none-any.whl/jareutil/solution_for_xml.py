class SolutionForXML(object):
    
    def __init__(self, guid, parameters, metadata = None, number_of_pameters = None ):
        assert guid != None, "Argument 'guid' can't be None"
        self.guid = guid
        assert parameters != None, "Argument 'parameters' can't be None"
        self.parameters = parameters
        if number_of_pameters != None:
            assert len(parameters) == number_of_pameters, "Argument 'number_of_pameters' has value " + str(number_of_pameters) + " but parameters length is " + str(len(parameters)) + "."
        self.number_of_pameters = number_of_pameters
        self.metadata = metadata
                
    def __len__(self):
        return len(self.parameters)

