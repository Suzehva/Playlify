import React from 'react';
import { Flex } from '@chakra-ui/react';
import PlayifyForm from './PlayifyForm'; // Adjust import path as necessary

function App() {
  return (
    <Flex
      height="100vh"
      align="center"
      justify="center"
      bg="gray.100" // Optional: background color for better visibility
    >
      <PlayifyForm />
    </Flex>
  );
}

export default App;
