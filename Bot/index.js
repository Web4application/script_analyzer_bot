client.on('interactionCreate', async interaction => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === 'analyze') {
    const text = interaction.options.getString('text');

    try {
      const response = await axios.post('http://localhost:3000/api/analyze', { text });
      const result = response.data.analysis;
      await interaction.reply(`Analysis: ${result}`);
    } catch (error) {
      console.error('Analysis failed:', error.message);
      await interaction.reply('Something went wrong analyzing the text.');
    }
  }
});
