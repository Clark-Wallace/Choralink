// Choralink Visual Score Component (React)

import React, { useEffect, useRef } from 'react';
import { OpenSheetMusicDisplay } from 'opensheetmusicdisplay';
import './VisualScore.css';

/**
 * VisualScore component for rendering sheet music
 * 
 * This component uses OpenSheetMusicDisplay to render MusicXML content
 * and provides controls for zooming and navigation.
 * 
 * @param {Object} props Component props
 * @param {string|Object} props.sheetData MusicXML string or object with musicxml property
 * @param {Object} props.options Display options
 */
export default function VisualScore({ sheetData, options = {} }) {
    const divRef = useRef(null);
    const osmdRef = useRef(null);
    
    useEffect(() => {
        if (divRef.current && sheetData) {
            if (!osmdRef.current) {
                osmdRef.current = new OpenSheetMusicDisplay(divRef.current);
            }
            
            // Configure display options
            osmdRef.current.setOptions({
                followCursor: options.followCursor || true,
                drawTitle: options.drawTitle || true,
                drawSubtitle: options.drawSubtitle || true,
                drawComposer: options.drawComposer || true,
                drawCredits: options.drawCredits || true,
                ...options
            });
            
            // Load and render the sheet music
            if (typeof sheetData === 'string') {
                // If sheetData is a MusicXML string
                osmdRef.current.load(sheetData)
                    .then(() => {
                        osmdRef.current.render();
                    })
                    .catch(error => {
                        console.error("Error rendering sheet music:", error);
                    });
            } else if (sheetData.musicxml) {
                // If sheetData is an object with musicxml property
                osmdRef.current.load(sheetData.musicxml)
                    .then(() => {
                        osmdRef.current.render();
                    })
                    .catch(error => {
                        console.error("Error rendering sheet music:", error);
                    });
            }
        }
    }, [sheetData, options]);
    
    return (
        <div className="visual-score-container">
            <div className="visual-score" ref={divRef}></div>
            {options.showControls && (
                <div className="score-controls">
                    <button onClick={() => osmdRef.current?.zoom(1.2)}>Zoom In</button>
                    <button onClick={() => osmdRef.current?.zoom(0.8)}>Zoom Out</button>
                    {/* Add more controls as needed */}
                </div>
            )}
        </div>
    );
}
