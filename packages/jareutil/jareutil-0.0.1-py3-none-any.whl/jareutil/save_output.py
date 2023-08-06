from xml.etree.ElementTree import Element, SubElement, ElementTree
from jareutil.evaluation_result import EvaluationResult

def save_output(evalution_results, file_path = 'output.xml'):
    assert type(evalution_results) is list or type(evalution_results) is EvaluationResult, "Argument 'evalution_results' is 'EvaluationResult' or 'list', but get type " + str(type(evalution_results)) + '.'
    if type(evalution_results) is EvaluationResult:
        evalution_results = [evalution_results]
    root = Element('ArrayOfEvaluationResult')
    for out in evalution_results:
        eval_result = Element('EvaluationResult')

        status = SubElement(eval_result, 'Status')
        status.text = out.status

        message = SubElement(eval_result, 'Message')
        message.text = out.message

        variables = SubElement(eval_result, 'Variables')
        for variable in out.variables:
            varialble_element = SubElement(variables, 'double')
            varialble_element.text = str(variable)

        result = SubElement(eval_result, 'Result')
        for goal in out.result:
            result_element = SubElement(result, 'double')
            result_element.text = str(goal)

        metadata = SubElement(eval_result, 'Metadata')
        metadata.text = out.metadata

        guid = SubElement(eval_result, 'Guid')
        guid.text = str(out.guid)
        
        root.append(eval_result)
    
        with open(file_path, 'wb') as f:
            ElementTree(root).write(f)
