// TestChakra.js
import React from 'react';
import { ChakraProvider, Box, Text, Button, Heading, Stack } from '@chakra-ui/react';

function TestChakra() {
  return (
    <ChakraProvider>
      <Box padding="4" maxWidth="600px" margin="auto">
        <Heading as="h1" size="xl" textAlign="center" mb="4">
          Chakra UI Test
        </Heading>
        <Stack spacing="4">
          <Box bg="teal.100" p="4" borderRadius="md">
            <Text fontSize="lg" color="teal.800">
              This is a Box with a teal background.
            </Text>
          </Box>
          <Button colorScheme="blue" size="lg" variant="solid">
            Test Button
          </Button>
          <Button colorScheme="red" size="md" variant="outline">
            Another Test Button
          </Button>
        </Stack>
      </Box>
    </ChakraProvider>
  );
}

export default TestChakra;
