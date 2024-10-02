import React from 'react';
import {
  Box,
  Heading,
  Text,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
} from '@chakra-ui/react';

const DashboardPage = () => {
  return (
    <Box maxWidth="1200px" margin="auto" mt={8} p={4}>
      <Heading as="h1" size="xl" mb={6}>
        Hotel Campaign Dashboard
      </Heading>
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
        <Stat>
          <StatLabel>Current Occupancy Rate</StatLabel>
          <StatNumber>65%</StatNumber>
          <StatHelpText>Feb 12 - Feb 28</StatHelpText>
        </Stat>
        <Stat>
          <StatLabel>Forecasted Occupancy</StatLabel>
          <StatNumber>72%</StatNumber>
          <StatHelpText>Next 30 days</StatHelpText>
        </Stat>
        <Stat>
          <StatLabel>Active Campaigns</StatLabel>
          <StatNumber>3</StatNumber>
          <StatHelpText>2 ending this week</StatHelpText>
        </Stat>
      </SimpleGrid>
      <Box mt={10}>
        <Heading as="h2" size="lg" mb={4}>
          Recent Activity
        </Heading>
        <Text>Campaign "Summer Special" launched yesterday</Text>
        <Text>Occupancy forecast updated 2 hours ago</Text>
        <Text>New customer segment identified: "Weekend Travelers"</Text>
      </Box>
      <Box mt={10}>
        <Heading as="h2" size="lg" mb={4}>
          Upcoming Actions
        </Heading>
        <Text>Optimize pricing for next month (due in 3 days)</Text>
        <Text>Review customer feedback for Q1 (due next week)</Text>
        <Text>Plan marketing budget for Q3 (due in 2 weeks)</Text>
      </Box>
    </Box>
  );
};

export default DashboardPage;
