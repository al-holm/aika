GERMAN_ANSWER_API = {
    'summary': 'Get answer from the german learning agent',
    'parameters': [
        {
            'name': 'question',
            'in': 'body',
            'required': True,
            'description': 'Question for the agent',
            'schema': {
                'type': 'object',
                'properties': {
                    'question': {
                        'type': 'string',
                        'example': 'What is the Partizip II of gehen?'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'A response with the agent\'s answer.',
            'schema': { 'type': 'object', 
                       'properties': { 
                           'answer': {
                                'type': 'string',
                                'example': 'Gegangen is the Partizip II of gehen.'
                            }
                       }
            },
        },
    }
}

LAW_ANSWER_API = {
    'summary': 'Get answer from the agent (immigration law and everyday life counseling)',
    'parameters': [
        {
            'name': 'question',
            'in': 'body',
            'required': True,
            'description': 'Question for the agent',
            'schema': {
                'type': 'object',
                'properties': {
                    'question': {
                        'type': 'string',
                        'example': 'Was soll ich vor der Anhörung wissen?'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'A response with the agent\'s answer.',
            'schema': { 'type': 'object', 
                       'properties': { 
                           'answer': {
                                'type': 'string',
                                'example': 'Vor der Anhörung solltest du dich gut verbereiten. Folgendes ist zu beachten...'
                            }
                       }
            },
        },
    }
}

LESSON_API = {
    'summary': 'Get generated lesson unit with exercises for a lesson',
    'parameters': [
        {
            'name': 'question',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'question': {
                        'type': 'string',
                        'example': '[Grammar|Listening|Reading][Topic][Subtopic][#single-choice][#fill-the-gaps][#open question]'
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'A successful response with the generated exercises.',
            'schema': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'example': 'Dieses Jahr war Jacob in Griechenland...'
                    },
                    'tasks': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'type': {
                                    'type': 'string',
                                    'example': 'single-choice'
                                },
                                'question': {
                                    'type': 'string',
                                    'example': 'In welchem Land hat Jacob sein Urlaub verbracht?'
                                },
                                'answer_options': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string',
                                        'example': 'Italien, Griechenland, Deutchland',
                                    }
                                },
                                'solution': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string',
                                        'example': 'Griechenland'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}