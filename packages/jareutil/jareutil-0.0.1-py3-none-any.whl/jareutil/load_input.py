import xml.etree.ElementTree as ET
from jareutil.solution_for_xml import SolutionForXML

def laod_input(file_path = 'input.xml'):
    tree = ET.parse(file_path)
    root = tree.getroot()
    evaluator_inputs = []
    solutions = root.findall('SolutionForXML')
    for solution in solutions:
        guid = solution.find('Guid').text
        parameters = list(map(lambda x: float(x.text), solution.find('Parameters').findall('double')))
        metadata = solution.find("Metadata")
        if metadata != None:
            metadata = metadata.text
        number_of_parameters = int(solution.find('NumOfPar').text)
        solution_input = SolutionForXML(guid, parameters,metadata, number_of_parameters)
        evaluator_inputs.append(solution_input)
    return evaluator_inputs