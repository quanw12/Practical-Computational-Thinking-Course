import React, { useState } from 'react';

interface TranslationPanelProps {
  // Optional props for future expansion
}

const TranslationPanel: React.FC<TranslationPanelProps> = () => {
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const translateText = async () => {
    if (!inputText.trim()) {
      setError('Please enter some English text to translate');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: inputText.trim(),
          source_lang: 'en',
          target_lang: 'vi'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        setTranslatedText(data.translated_text);
      } else {
        throw new Error(data.message || 'Translation failed');
      }

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(`Translation error: ${errorMessage}`);
      console.error('Translation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearTranslation = () => {
    setInputText('');
    setTranslatedText('');
    setError(null);
  };

  return (
    <div className="translation-panel">
      <div className="translation-header">
        <h3>🔤 English → Vietnamese Translator</h3>
        <p>Enter English text and get instant Vietnamese translation</p>
      </div>
      
      <div className="translation-container">
        <div className="input-section">
          <label htmlFor="english-input">English Text:</label>
          <textarea
            id="english-input"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter English text here... (e.g., 'Hello, how are you?')"
            className="translation-input"
            rows={3}
            disabled={loading}
          />
        </div>

        <div className="translation-controls">
          <button 
            onClick={translateText}
            className="translate-btn"
            disabled={loading || !inputText.trim()}
          >
            {loading ? 'Translating...' : '🌐 Translate'}
          </button>
          
          <button 
            onClick={clearTranslation}
            className="clear-btn"
            disabled={loading}
          >
            🗑️ Clear
          </button>
        </div>

        {loading && (
          <div className="translation-loading">
            Translating your text to Vietnamese...
          </div>
        )}

        {error && (
          <div className="translation-error">
            {error}
          </div>
        )}

        {translatedText && !loading && (
          <div className="output-section">
            <label htmlFor="vietnamese-output">Vietnamese Translation:</label>
            <textarea
              id="vietnamese-output"
              value={translatedText}
              readOnly
              className="translation-output"
              rows={3}
            />
            <div className="translation-info">
              <small>✅ Translation completed successfully!</small>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TranslationPanel;