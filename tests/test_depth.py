import unittest
from unittest.mock import MagicMock, patch

from graphql import GraphQLCoreBackend
from graphql.language.ast import FragmentDefinition
from graphene.test import Client
from examples.starwars.schema import schema

from secure_graphene.depth import (
    measure_depth,
    DepthAnalysisBackend,
    DepthLimitReached,
    get_fragments,
    get_queries_and_mutations,
)


class GetFragmentsTest(unittest.TestCase):
    def test_when_no_fragments_expect_empty_dict(self):
        query = """            
            query {
              luke: human(id: "1000") {
                name
                friends {
                  name
                  friends {
                    name
                    friends {
                      name 
                    }
                  }
                }
              }
              leia: human(id: "1003") {
                name
                friends {
                  name
                  friends {
                    name
                  }
                }
              }
            }
        """
        document = GraphQLCoreBackend().document_from_string(
            schema=schema, document_string=query
        )
        definitions = document.document_ast.definitions

        fragments = get_fragments(definitions=definitions)

        expect = 0
        result = len(fragments)

        self.assertEqual(expect, result)

    def test_when_two_fragments_expect_two_items_in_dict(self):
        query = """
            query {
              hero {
                ...nameFragment
                ...friendsFragment
              }
            }

            fragment nameFragment on Character {
              name
            }
            fragment friendsFragment on Character {
              friends {
                name
              }
            }
        """
        document = GraphQLCoreBackend().document_from_string(
            schema=schema, document_string=query
        )
        definitions = document.document_ast.definitions

        fragments = get_fragments(definitions=definitions)

        expect = 2
        result = len(fragments)
        expect_key = "nameFragment"
        expect_class = FragmentDefinition
        result_object = fragments.get(expect_key)

        self.assertEqual(expect, result)
        self.assertIsInstance(result_object, expect_class)


class GetQueriesTest(unittest.TestCase):
    def test_when_two_operation_definitions_expect_two_items(self):
        query = """            
            query {
              luke: human(id: "1000") {
                name
              }
            }            
            query {
              leia: human(id: "1003") {
                name
              }
            }
        """
        document = GraphQLCoreBackend().document_from_string(
            schema=schema, document_string=query
        )
        definitions = document.document_ast.definitions

        queries = get_queries_and_mutations(definitions=definitions)

        expect = 2
        result = len(queries)

        self.assertEqual(expect, result)

    def test_when_two_fragments_expect_two_items_in_dict(self):
        query = """
            query {
              hero {
                ...nameFragment
                ...friendsFragment
              }
            }

            fragment nameFragment on Character {
              name
            }
            fragment friendsFragment on Character {
              friends {
                name
              }
            }
        """
        document = GraphQLCoreBackend().document_from_string(
            schema=schema, document_string=query
        )
        definitions = document.document_ast.definitions

        fragments = get_fragments(definitions=definitions)

        expect = 2
        result = len(fragments)
        expect_key = "nameFragment"
        expect_object = FragmentDefinition
        result_object = fragments.get(expect_key)

        self.assertEqual(expect, result)
        self.assertIsInstance(result_object, expect_object)


class MeasureDepthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client(schema)

    def test_when_depth_is_5_expect_measure_5_depth(self):
        query = """            
            query {
              luke: human(id: "1000") {
                name
                friends {
                  name
                  friends {
                    name
                    friends {
                      name 
                    }
                  }
                }
              }
              leia: human(id: "1003") {
                name
                friends {
                  name
                  friends {
                    name
                  }
                }
              }
            }
        """
        document = GraphQLCoreBackend().document_from_string(
            schema=schema, document_string=query
        )
        node = document.document_ast.definitions[0]

        result_depth = measure_depth(node=node, fragments={})
        expected_depth = 5

        self.assertEqual(expected_depth, result_depth)

    def test_when_depth_is_2_expect_measure_2_depth(self):
        query = """
            query {
              hero {
                name
              }
            }
        """
        document = GraphQLCoreBackend().document_from_string(
            schema=schema, document_string=query
        )
        node = document.document_ast.definitions[0]

        result_depth = measure_depth(node=node, fragments={})
        expected_depth = 2

        self.assertEqual(expected_depth, result_depth)

    def test_when_introspection_expect_measure_0_depth(self):
        query = """
            query IntrospectionQuery {
              __schema {
                queryType {
                  name
                }
                mutationType {
                  name
                }
                subscriptionType {
                  name
                }
                types {
                  ...FullType
                }
                directives {
                  name
                  description
                  locations
                  args {
                    ...InputValue
                  }
                }
              }
            }

            fragment FullType on __Type {
              kind
              name
              description
              fields(includeDeprecated: true) {
                name
                description
                args {
                  ...InputValue
                }
                type {
                  ...TypeRef
                }
                isDeprecated
                deprecationReason
              }
              inputFields {
                ...InputValue
              }
              interfaces {
                ...TypeRef
              }
              enumValues(includeDeprecated: true) {
                name
                description
                isDeprecated
                deprecationReason
              }
              possibleTypes {
                ...TypeRef
              }
            }

            fragment InputValue on __InputValue {
              name
              description
              type {
                ...TypeRef
              }
              defaultValue
            }

            fragment TypeRef on __Type {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                    ofType {
                      kind
                      name
                      ofType {
                        kind
                        name
                        ofType {
                          kind
                          name
                          ofType {
                            kind
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
        """
        document = GraphQLCoreBackend().document_from_string(
            schema=schema, document_string=query
        )
        node = document.document_ast.definitions[0]

        result_depth = measure_depth(node=node, fragments={})
        expected_depth = 0

        self.assertEqual(expected_depth, result_depth)

    def test_when_introspection_and_query_expect_measure_2_depth(self):
        query = """
            query {
              hero {
                name
              }
            }
            query IntrospectionQuery {
              __schema {
                queryType {
                  name
                }
                mutationType {
                  name
                }
                subscriptionType {
                  name
                }
                types {
                  ...FullType
                }
                directives {
                  name
                  description
                  locations
                  args {
                    ...InputValue
                  }
                }
              }
            }

            fragment FullType on __Type {
              kind
              name
              description
              fields(includeDeprecated: true) {
                name
                description
                args {
                  ...InputValue
                }
                type {
                  ...TypeRef
                }
                isDeprecated
                deprecationReason
              }
              inputFields {
                ...InputValue
              }
              interfaces {
                ...TypeRef
              }
              enumValues(includeDeprecated: true) {
                name
                description
                isDeprecated
                deprecationReason
              }
              possibleTypes {
                ...TypeRef
              }
            }

            fragment InputValue on __InputValue {
              name
              description
              type {
                ...TypeRef
              }
              defaultValue
            }

            fragment TypeRef on __Type {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                    ofType {
                      kind
                      name
                      ofType {
                        kind
                        name
                        ofType {
                          kind
                          name
                          ofType {
                            kind
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
        """
        document = GraphQLCoreBackend().document_from_string(
            schema=schema, document_string=query
        )
        node = document.document_ast.definitions[0]

        result_depth = measure_depth(node=node, fragments={})
        expected_depth = 2

        self.assertEqual(expected_depth, result_depth)


class DepthAnalysisBackendTest(unittest.TestCase):
    @patch("secure_graphene.depth.measure_depth", MagicMock(return_value=3))
    def test_when_max_depth_is_2_and_measure_3_expect_depth_limit_reached_exception(
            self
    ):
        query = """
            query {
              __schema 
              queryType {
                name
              }
            }

            query {
              hero {
                name
                friends {
                  name
                }
              }
            }
        """
        backend = DepthAnalysisBackend(max_depth=2)

        with self.assertRaises(DepthLimitReached):
            backend.document_from_string(schema=schema, document_string=query)

    @patch("secure_graphene.depth.measure_depth", MagicMock(return_value=3))
    def test_when_max_depth_is_5_and_measure_3_expect_no_errors(self):
        query = """
            query {
              hero {
                ...heroNameAndFriends
              }
            }

            fragment heroNameAndFriends on Character {
              name
              friends {
                name
              }
            }
        """
        backend = DepthAnalysisBackend(max_depth=5)

        document = backend.document_from_string(
            schema=schema, document_string=query
        )

        self.assertIsNotNone(document)
