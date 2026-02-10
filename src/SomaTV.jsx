import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";

export default function SomaTV() {
  const [movies, setMovies] = useState([]);
  const [isAiOn, setIsAiOn] = useState(false);
  const [mood, setMood] = useState("Neutral");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Replace this with your actual TMDB API Key
  const API_KEY = "YOUR_TMDB_API_KEY_HERE";

  // Genre mapping based on TMDB standards
  const genresMap = {
    28: "Action",
    878: "Sci-Fi",
    35: "Comedy",
    18: "Drama",
    27: "Horror",
    16: "Animation",
  };

  const fetchMovies = async () => {
    try {
      const pages = [1, 2, 3, 4, 5]; // Fetch multiple pages for better variety
      const responses = await Promise.all(
        pages.map((p) =>
          axios.get(
            `https://api.themoviedb.org/3/movie/popular?api_key=${API_KEY}&page=${p}`,
          ),
        ),
      );

      const allResults = responses.flatMap((r) => r.data.results);

      const formatted = allResults.map((m) => {
        // Determine the primary genre from the API results
        let genre = "Action";
        if (m.genre_ids.includes(35)) genre = "Comedy";
        else if (m.genre_ids.includes(878)) genre = "Sci-Fi";
        else if (m.genre_ids.includes(18)) genre = "Drama";
        else if (m.genre_ids.includes(27)) genre = "Horror";
        else if (m.genre_ids.includes(16)) genre = "Animation";

        // Map specific genres to AI moods logically
        let movieMood = "Neutral";
        if (genre === "Comedy") movieMood = "Happy";
        else if (genre === "Horror") movieMood = "Fear";
        else if (genre === "Action")
          movieMood = Math.random() > 0.5 ? "Angry" : "Neutral";
        else if (genre === "Drama") movieMood = "Sad";

        return {
          id: m.id,
          name: m.title,
          year: m.release_date?.split("-")[0] || "2026",
          genre: genre,
          mood: movieMood,
          img: `https://image.tmdb.org/t/p/w500${m.poster_path}`,
          backdrop: `https://image.tmdb.org/t/p/original${m.backdrop_path}`,
        };
      });

      // Remove duplicates and update state
      const uniqueMovies = Array.from(
        new Map(formatted.map((item) => [item.id, item])).values(),
      );
      setMovies(uniqueMovies);
    } catch (e) {
      console.error("TMDB API Error:", e);
    }
  };

  const captureAndPredict = async () => {
    if (!isAiOn || !videoRef.current || !canvasRef.current) return;
    const canvas = canvasRef.current;
    canvas.width = 100;
    canvas.height = 100;
    canvas.getContext("2d").drawImage(videoRef.current, 0, 0, 100, 100);
    const base64Image = canvas.toDataURL("image/jpeg").split(",")[1];
    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", {
        image: base64Image,
      });
      if (response.data.mood) setMood(response.data.mood);
    } catch (err) {
      console.error("AI Backend Offline");
    }
  };

  useEffect(() => {
    fetchMovies();
  }, []);

  useEffect(() => {
    if (isAiOn) {
      navigator.mediaDevices.getUserMedia({ video: true }).then((s) => {
        if (videoRef.current) videoRef.current.srcObject = s;
      });
      const interval = setInterval(captureAndPredict, 3000); // Analyze emotion every 3 seconds
      return () => clearInterval(interval);
    } else {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
      }
    }
  }, [isAiOn]);

  const filteredMovies = movies.filter((movie) => {
    const matchesSearch = movie.name
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    const matchesCategory =
      selectedCategory === "All" || movie.genre === selectedCategory;
    const matchesAiMood = !isAiOn || movie.mood === mood;
    return matchesSearch && matchesCategory && matchesAiMood;
  });

  return (
    <div className="min-h-screen bg-[#050508] text-white font-sans selection:bg-red-600">
      <video ref={videoRef} className="hidden" autoPlay />
      <canvas ref={canvasRef} className="hidden" />

      <header className="fixed top-0 w-full z-[100] px-8 py-4 flex justify-between items-center bg-black/80 backdrop-blur-xl border-b border-white/5">
        <div className="text-3xl font-black italic text-red-600 tracking-tighter uppercase">
          SOMA<span className="text-white">TV</span>
        </div>
        <div className="flex items-center gap-6 flex-1 justify-end max-w-3xl">
          <input
            type="text"
            placeholder="Search titles, genres..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full max-w-md bg-zinc-900/80 border border-zinc-800 rounded-full px-6 py-2 text-sm focus:ring-2 focus:ring-red-600 outline-none"
          />
          <button
            onClick={() => setIsAiOn(!isAiOn)}
            className={`px-5 py-2 rounded-full font-bold text-[10px] uppercase transition-all ${isAiOn ? "bg-red-600 text-white" : "bg-zinc-800 text-zinc-400"}`}
          >
            AI MODE: {isAiOn ? mood : "OFF"}
          </button>
        </div>
      </header>

      <main className="pt-28 px-10">
        <div className="flex gap-4 overflow-x-auto pb-8 no-scrollbar">
          {[
            "All",
            "Action",
            "Sci-Fi",
            "Comedy",
            "Drama",
            "Horror",
            "Animation",
          ].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-6 py-2 rounded-xl text-xs font-bold transition-all ${selectedCategory === cat ? "bg-white text-black" : "bg-zinc-900 text-zinc-500 border border-zinc-800"}`}
            >
              {cat}
            </button>
          ))}
        </div>

        {filteredMovies.length > 0 && (
          <section className="relative h-[480px] rounded-[40px] overflow-hidden mb-16 shadow-2xl border border-white/5 group">
            <img
              src={filteredMovies[0].backdrop}
              className="w-full h-full object-cover opacity-40 group-hover:scale-105 transition-all duration-1000"
              alt="Hero"
            />
            <div className="absolute inset-0 bg-gradient-to-r from-black via-black/20 to-transparent" />
            <div className="absolute bottom-12 left-12">
              <h1 className="text-6xl font-black uppercase italic mb-4">
                {filteredMovies[0].name}
              </h1>
              <div className="flex gap-4 mb-6 text-xs font-bold">
                <span className="text-green-500 uppercase tracking-widest">
                  98% Match
                </span>
                <span className="text-zinc-400">{filteredMovies[0].year}</span>
                <span className="border border-white/20 px-3 py-1 rounded uppercase">
                  {filteredMovies[0].genre}
                </span>
              </div>
              <button className="bg-white text-black px-10 py-3 rounded-2xl font-black uppercase text-[10px] hover:bg-red-600 hover:text-white transition-all">
                ▶ Play Now
              </button>
            </div>
          </section>
        )}

        <h2 className="text-xl font-black uppercase italic mb-8 border-l-4 border-red-600 pl-4 tracking-widest">
          {isAiOn ? `AI Selection: ${mood}` : `${selectedCategory} Collection`}
        </h2>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-8">
          <AnimatePresence mode="popLayout">
            {filteredMovies.map((movie) => (
              <motion.div
                key={movie.id}
                layout
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className={`relative aspect-[2/3] rounded-[30px] overflow-hidden border-2 group cursor-pointer ${isAiOn ? "border-red-600 shadow-[0_0_20px_rgba(220,38,38,0.3)]" : "border-transparent"}`}
              >
                <img
                  src={movie.img}
                  className="w-full h-full object-cover"
                  alt={movie.name}
                />
                <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-all flex flex-col justify-end p-6">
                  <p className="text-[10px] font-black uppercase">
                    {movie.name}
                  </p>
                  <p className="text-[8px] text-zinc-400 mt-1">
                    {movie.genre} • {movie.year}
                  </p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </main>

      <footer className="border-t border-white/5 bg-black/40 pt-20 pb-12 px-16 mt-20 text-center">
        <div className="text-2xl font-black italic text-red-600 mb-4 uppercase">
          SOMA<span className="text-white">TV</span>
        </div>
        <p className="text-zinc-600 text-[8px] font-black uppercase tracking-[0.5em]">
          © 2026 SOMATV - AI DRIVEN STREAMING
        </p>
      </footer>
    </div>
  );
}
