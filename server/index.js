
const express = require('express');
const path = require('path');
const app = express();
const PORT = 1573;

app.use(express.json());
app.use(express.static(path.join(__dirname, '../frontend')));

app.post('/api/login', (req, res) => {
  const { id, pw } = req.body;

  if(id === 'admin' && pw === '1234'){
    return res.json({ success: true, token: 'demo-token' });
  }

  return res.status(401).json({ success: false });
});

app.listen(PORT, () => {
  console.log('SERVER RUNNING ON ' + PORT);
});
