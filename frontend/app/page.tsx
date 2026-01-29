"use client";
import { useState } from 'react';
import axios from 'axios';
import { Send, Cpu, Share2 } from 'lucide-react';
import Image from "next/image";


export default function Home() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<{role: string, text: string}[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setMessages(prev => [...prev, { role: 'user', text: query }]);

    try {
      const res = await axios.post('http://localhost:8000/chat', { query });
      setMessages(prev => [...prev, { role: 'ai', text: res.data.answer }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'ai', text: "Error connecting to Nexus core." }]);
    }
    setLoading(false);
    setQuery('');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col items-center p-10 font-mono">
      {/* Header */}
      <div className="flex items-center gap-3 mb-10">
        <Share2 className="w-10 h-10 text-yellow-400" />
        <h1 className="text-4xl font-bold tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-red-600">
          Anima
        </h1>
      </div>

      {/* Main Graph/Chat Container */}
      <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-6 h-[600px]">
        
        {/* Left: Chat Interface */}
        <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-cyan-500 to-blue-500" />
          
          <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
            {messages.length === 0 && (
              <div className="text-slate-500 text-center mt-20">
                <Cpu className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>Initialize query sequence...</p>
                <p className="text-xs mt-2">Try: "Who maintains the Payment Gateway?"</p>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`p-3 rounded-lg max-w-[80%] ${m.role === 'user' ? 'bg-cyan-900/30 ml-auto border border-cyan-800' : 'bg-slate-800 border border-slate-700'}`}>
                <p className="text-sm">{m.text}</p>
              </div>
            ))}
            {loading && <div className="text-cyan-400 animate-pulse text-xs">Accessing Neural Graph...</div>}
          </div>

          <div className="flex gap-2">
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 focus:outline-none focus:border-cyan-500 transition-colors"
              placeholder="Query the institutional memory..."
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button onClick={handleSearch} className="bg-cyan-600 hover:bg-cyan-500 text-white p-2 rounded-lg transition-all">
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Right: Context/Graph Visualization Placeholder */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 hidden md:flex flex-col">
          <h2 className="text-xs uppercase tracking-widest text-slate-500 mb-4">Active Nodes</h2>
          <div className="flex-1 flex items-center justify-center border border-dashed border-slate-800 rounded-lg">
             {/* In a real project, use 'react-force-graph' here */}
             <div className="text-center opacity-40">
                <div className="w-20 h-20 rounded-full border-2 border-cyan-500 mx-auto flex items-center justify-center mb-2">
                    <Share2 className="w-10 h-10" />
                </div>
                <p className="text-xs">Graph Visualization Active</p>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// export default function Home() {
//   return (
//     <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
//       <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
//         <Image
//           className="dark:invert"
//           src="/next.svg"
//           alt="Next.js logo"
//           width={100}
//           height={20}
//           priority
//         />
//         <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
//           <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
//             To get started, edit the page.tsx file.
//           </h1>
//           <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
//             Looking for a starting point or more instructions? Head over to{" "}
//             <a
//               href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//               className="font-medium text-zinc-950 dark:text-zinc-50"
//             >
//               Templates
//             </a>{" "}
//             or the{" "}
//             <a
//               href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//               className="font-medium text-zinc-950 dark:text-zinc-50"
//             >
//               Learning
//             </a>{" "}
//             center.
//           </p>
//         </div>
//         <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
//           <a
//             className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
//             href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             <Image
//               className="dark:invert"
//               src="/vercel.svg"
//               alt="Vercel logomark"
//               width={16}
//               height={16}
//             />
//             Deploy Now
//           </a>
//           <a
//             className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
//             href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Documentation
//           </a>
//         </div>
//       </main>
//     </div>
//   );
// }
