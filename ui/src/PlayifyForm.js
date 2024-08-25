import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Heading,
  VStack,
  useToast
} from '@chakra-ui/react';

function PlayifyForm() {
  const [context, setContext] = useState('');
  const [mood, setMood] = useState('');
  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const queryParams = new URLSearchParams({
      context: context,
      mood: mood
    }).toString();

    try {
      const response = await fetch(`/main?${queryParams}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const result = await response.text();
        toast({
          title: 'Success!',
          description: 'Playlist created successfully.',
          status: 'success',
          duration: 9000,
          isClosable: true,
        });
      } else {
        toast({
          title: 'Error!',
          description: `Server responded with status: ${response.status}`,
          status: 'error',
          duration: 9000,
          isClosable: true,
        });
      }
    } catch (error) {
      toast({
        title: 'Error!',
        description: 'An error occurred while creating the playlist.',
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
    }
  };

  return (
    <Box
      padding="20px"
      maxWidth="500px"
      width="100%"
      backgroundColor="white"
      borderRadius="md"
      boxShadow="md"
      margin="auto"
      display="flex"
      flexDirection="column"
      alignItems="center"
    >
      <Heading as="h2" size="lg" textAlign="center" mb="20px">
        Playify: Create a message hidden in a playlist
      </Heading>
      <form onSubmit={handleSubmit} style={{ width: '100%' }}>
        <VStack spacing="20px" align="stretch">
          <FormControl>
            <FormLabel htmlFor="context" textAlign="center">Give us some context!</FormLabel>
            <Input
              type="text"
              id="context"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="I want to propose to my girlfriend"
              textAlign="center"  // Center the text and placeholder
            />
          </FormControl>
          <FormControl>
            <FormLabel htmlFor="mood" textAlign="center">Mood</FormLabel>
            <Input
              type="text"
              id="mood"
              value={mood}
              onChange={(e) => setMood(e.target.value)}
              placeholder="love"
              textAlign="center"  // Center the text and placeholder
            />
          </FormControl>
          <Button
            type="submit"
            colorScheme="blue"
            size="lg"
            variant="solid"
          >
            Submit
          </Button>
        </VStack>
      </form>
    </Box>
  );
}

export default PlayifyForm;
