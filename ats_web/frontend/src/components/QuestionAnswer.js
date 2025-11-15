import React, { useState } from 'react';
import SpeakButton from './SpeakButton';
import { MessageCircle, Send } from 'lucide-react';

const QuestionAnswer = () => {
  const [question, setQuestion] = useState('');
  const [conversations, setConversations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleAskQuestion = async () => {
    if (!question.trim()) return;

    const userMessage = {
      type: 'question',
      text: question,
      timestamp: new Date().toISOString()
    };

    setConversations(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Here you would call your actual Q&A API
      // For now, this is a placeholder response
      const response = await generateAnswer(question);
      
      const answerMessage = {
        type: 'answer',
        text: response,
        timestamp: new Date().toISOString()
      };

      setConversations(prev => [...prev, answerMessage]);
      
    } catch (error) {
      console.error('Error getting answer:', error);
      const errorMessage = {
        type: 'answer',
        text: 'Sorry, I encountered an error processing your question.',
        timestamp: new Date().toISOString()
      };
      setConversations(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setQuestion('');
    }
  };

  const generateAnswer = async (question) => {
    // Placeholder - replace with your actual API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    return `This is a sample answer to: "${question}". Replace this with your actual Q&A logic.`;
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-t-lg">
          <div className="flex items-center gap-2">
            <MessageCircle size={24} />
            <h2 className="text-xl font-semibold">Ask Questions</h2>
          </div>
          <p className="text-sm text-blue-100 mt-1">
            Ask questions and hear the answers with text-to-speech
          </p>
        </div>

        {/* Conversation Area */}
        <div className="p-4 space-y-4 min-h-[400px] max-h-[600px] overflow-y-auto">
          {conversations.length === 0 ? (
            <div className="text-center text-gray-400 py-12">
              <MessageCircle size={48} className="mx-auto mb-4 opacity-50" />
              <p>No questions yet. Ask something to get started!</p>
            </div>
          ) : (
            conversations.map((msg, index) => (
              <div
                key={index}
                className={`flex gap-3 ${
                  msg.type === 'question' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    msg.type === 'question'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className="flex-1">
                      <p className="text-sm font-medium mb-1">
                        {msg.type === 'question' ? 'You' : 'Assistant'}
                      </p>
                      <p className="whitespace-pre-wrap">{msg.text}</p>
                    </div>
                    {msg.type === 'answer' && (
                      <SpeakButton text={msg.text} size="sm" />
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="flex gap-3 justify-start">
              <div className="bg-gray-100 rounded-lg p-4">
                <div className="flex items-center gap-2">
                  <div className="animate-pulse flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                  </div>
                  <span className="text-sm text-gray-500">Thinking...</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleAskQuestion()}
              placeholder="Ask a question..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
            <button
              onClick={handleAskQuestion}
              disabled={isLoading || !question.trim()}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 
                transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <Send size={18} />
              <span>Ask</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestionAnswer;
