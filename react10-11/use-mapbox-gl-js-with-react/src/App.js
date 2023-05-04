import React, { useRef, useEffect, useState } from 'react';
import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax

mapboxgl.accessToken = 'pk.eyJ1Ijoic2xlZXBsZXNzNDUxIiwiYSI6ImNsaDk0MnF1cDAzemgzbGxwamY4ajduOGQifQ.VSpTpgx4SjKm8nK5clke7w';

export default function App() {

    const mapContainer = useRef(null);
    const map = useRef(null);
    const popup = new mapboxgl.Popup();
    const [lng, setLng] = useState(30);
    const [lat, setLat] = useState(50);
    const [zoom, setZoom] = useState(7);

    useEffect(() => {
        if (map.current) return; // initialize map only once
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [lng, lat],
            zoom: zoom
        });
        map.current.on('click', (e) => {
            fetch(`http://localhost:5000/get_moisture_value?lat=${e.lngLat.lat}&lon=${e.lngLat.lng}`)
            .then(response => response.json())
            .then(data => {
                popup.setLngLat([e.lngLat.lng, e.lngLat.lat])
                .setHTML('Вологість: ' + data.moisture)
                .addTo(map.current);
            })
        });
    });

    useEffect(() => {
        if (!map.current) return; // wait for map to initialize
        map.current.on('move', () => {
            setLng(map.current.getCenter().lng.toFixed(4));
            setLat(map.current.getCenter().lat.toFixed(4));
            setZoom(map.current.getZoom().toFixed(2));
        })
    })

    return (
        <div>
            <div className="sidebar">
            Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
            </div>
            <div ref={mapContainer} className="map-container"/>
        </div>
    );
}