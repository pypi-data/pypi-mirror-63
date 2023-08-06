from uuid import UUID

class EvaluationResult(object):
    
    def __init__(self, guid, variables, result, metadata, status = "DONE", message = "OK"):
        super().__init__()
        assert guid != None, "Argument 'guid' has value None"
        assert variables != None, "Argument 'variables' has value None"
        assert result != None, "Argument 'result' has value None"
        assert metadata != None, "Argument 'metadata' has value None"
        assert status != None, "Argument 'status' has value None"
        assert message != None, "Argument 'message' has value None"
        assert type(guid) is str or type(guid) is UUID, "Argument 'guid' mast be type 'UUID' or string, but get type " + str(type(guid))
        assert type(variables) is list , "Argument 'variables' mast be type 'list', but get type " + str(type(variables))
        assert type(result) is list , "Argument 'result' mast be type 'list', but get type " + str(type(result))
        assert type(metadata) is str , "Argument 'metadata' mast be type 'string', but get type " + str(type(metadata))
        assert type(status) is str , "Argument 'status' mast be type 'string', but get type " + str(type(status))
        assert type(message) is str , "Argument 'message' mast be type 'string', but get type " + str(type(message))

        self.guid = guid
        self.variables = variables
        self.result = result
        self.metadata = metadata
        self.status = status
        self.message = message

        




