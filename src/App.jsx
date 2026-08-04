import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import HomeScreen from './components/HomeScreen';
import DasakamList from './components/DasakamList';
import SlokaView from './components/SlokaView';
import AudioPlayerBar from './components/AudioPlayerBar';

import narayaneeyamData from './data/narayaneeyam_data.json';

export default function App() {
  const [currentView, setCurrentView] = useState('home'); // 'home' | 'dasakams' | 'sloka'
  const [selectedDasakamId, setSelectedDasakamId] = useState(1);
  const [theme, setTheme] = useState('light');
  const [fontSizeMultiplier, setFontSizeMultiplier] = useState(1.0);
  
  // Audio state
  const [activeSloka, setActiveSloka] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isAutoplay, setIsAutoplay] = useState(true);

  // Apply theme to body
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Adjust font size
  const handleScaleFontSize = (delta) => {
    setFontSizeMultiplier(prev => Math.min(Math.max(0.8, prev + delta), 1.8));
  };

  // Navigate to Dasakam List
  const handleOpenNarayaneeyam = () => {
    setCurrentView('dasakams');
  };

  // Select a specific Dasakam
  const handleSelectDasakam = (id) => {
    setSelectedDasakamId(id);
    setCurrentView('sloka');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Back Navigation
  const handleBack = () => {
    if (currentView === 'sloka') {
      setCurrentView('dasakams');
    } else if (currentView === 'dasakams') {
      setCurrentView('home');
    }
  };

  // Close audio player bar
  const handleClosePlayer = () => {
    setActiveSloka(null);
    setIsPlaying(false);
  };

  // Get current selected Dasakam object
  const currentDasakam = narayaneeyamData.dasakams.find(d => d.id === selectedDasakamId) || narayaneeyamData.dasakams[0];

  // Play a specific sloka
  const handlePlaySloka = (dasakamNo, slokaNo) => {
    const dasakam = narayaneeyamData.dasakams.find(d => d.number === dasakamNo);
    if (!dasakam) return;

    const sloka = dasakam.slokas.find(s => s.slokaNo === slokaNo);
    if (!sloka) return;

    if (activeSloka?.dasakamNo === dasakamNo && activeSloka?.slokaNo === slokaNo) {
      // Toggle play/pause if clicking currently active sloka
      setIsPlaying(!isPlaying);
    } else {
      setActiveSloka({
        dasakamNo,
        slokaNo,
        text: sloka.text,
        audioUrl: sloka.audioUrl
      });
      setIsPlaying(true);
    }
  };

  // Play All Dasakam
  const handlePlayAll = (dasakamNo) => {
    const dasakam = narayaneeyamData.dasakams.find(d => d.number === dasakamNo);
    if (dasakam && dasakam.slokas.length > 0) {
      const firstSloka = dasakam.slokas[0];
      setActiveSloka({
        dasakamNo,
        slokaNo: firstSloka.slokaNo,
        text: firstSloka.text,
        audioUrl: firstSloka.audioUrl
      });
      setIsPlaying(true);
      setIsAutoplay(true);
    }
  };

  // Audio Next / Prev
  const handleNextSloka = () => {
    if (!activeSloka) return;
    const dasakam = narayaneeyamData.dasakams.find(d => d.number === activeSloka.dasakamNo);
    if (!dasakam) return;

    const currentIdx = dasakam.slokas.findIndex(s => s.slokaNo === activeSloka.slokaNo);
    if (currentIdx < dasakam.slokas.length - 1) {
      // Next sloka in same dasakam
      const nextSloka = dasakam.slokas[currentIdx + 1];
      setActiveSloka({
        dasakamNo: activeSloka.dasakamNo,
        slokaNo: nextSloka.slokaNo,
        text: nextSloka.text,
        audioUrl: nextSloka.audioUrl
      });
      setIsPlaying(true);
    } else {
      // Next Dasakam first sloka if available
      const nextDasakam = narayaneeyamData.dasakams.find(d => d.number === activeSloka.dasakamNo + 1);
      if (nextDasakam && nextDasakam.slokas.length > 0) {
        const nextSloka = nextDasakam.slokas[0];
        setSelectedDasakamId(nextDasakam.id);
        setActiveSloka({
          dasakamNo: nextDasakam.number,
          slokaNo: nextSloka.slokaNo,
          text: nextSloka.text,
          audioUrl: nextSloka.audioUrl
        });
        setIsPlaying(true);
      }
    }
  };

  const handlePrevSloka = () => {
    if (!activeSloka) return;
    const dasakam = narayaneeyamData.dasakams.find(d => d.number === activeSloka.dasakamNo);
    if (!dasakam) return;

    const currentIdx = dasakam.slokas.findIndex(s => s.slokaNo === activeSloka.slokaNo);
    if (currentIdx > 0) {
      const prevSloka = dasakam.slokas[currentIdx - 1];
      setActiveSloka({
        dasakamNo: activeSloka.dasakamNo,
        slokaNo: prevSloka.slokaNo,
        text: prevSloka.text,
        audioUrl: prevSloka.audioUrl
      });
      setIsPlaying(true);
    }
  };

  // Audio Ended -> Autoplay next
  const handleAudioEnded = () => {
    if (isAutoplay) {
      handleNextSloka();
    } else {
      setIsPlaying(false);
    }
  };

  // Title for Header
  let headerTitle = "Narayaneeyam App";
  if (currentView === "dasakams") headerTitle = "Narayaneeyam Dasakams";
  if (currentView === "sloka") headerTitle = `Dasakam ${currentDasakam?.number || 1}`;

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header
        currentView={currentView}
        title={headerTitle}
        onBack={handleBack}
        theme={theme}
        onToggleTheme={() => setTheme(t => t === 'light' ? 'dark' : 'light')}
        fontSize={fontSizeMultiplier}
        onChangeFontSize={handleScaleFontSize}
      />

      <main style={{ flex: 1 }}>
        {currentView === 'home' && (
          <HomeScreen
            onSelectNarayaneeyam={handleOpenNarayaneeyam}
            lastPlayedSloka={activeSloka}
            onPlaySloka={handlePlaySloka}
          />
        )}

        {currentView === 'dasakams' && (
          <DasakamList
            dasakams={narayaneeyamData.dasakams}
            onSelectDasakam={handleSelectDasakam}
          />
        )}

        {currentView === 'sloka' && (
          <SlokaView
            dasakam={currentDasakam}
            activeSloka={activeSloka}
            isPlaying={isPlaying}
            onPlaySloka={handlePlaySloka}
            onPlayAll={handlePlayAll}
            fontSizeMultiplier={fontSizeMultiplier}
          />
        )}
      </main>

      {/* Sticky Bottom Audio Player Bar */}
      <AudioPlayerBar
        activeSloka={activeSloka}
        isPlaying={isPlaying}
        onTogglePlay={() => setIsPlaying(!isPlaying)}
        onNext={handleNextSloka}
        onPrev={handlePrevSloka}
        onEnded={handleAudioEnded}
        isAutoplay={isAutoplay}
        onToggleAutoplay={() => setIsAutoplay(!isAutoplay)}
        onClose={handleClosePlayer}
      />
    </div>
  );
}
