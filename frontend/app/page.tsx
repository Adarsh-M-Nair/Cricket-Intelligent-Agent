"use client";

import { useEffect, useState } from "react";
import api from "../lib/api";

export default function Home() {
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    api
      .get("/health")
      .then((res) => setStatus(res.data.status))
      .catch(() => setStatus("Backend Error"));
  }, []);

  return (
    <main className="p-10">
      <h1 className="text-3xl font-bold">
        Cricket Intelligence Agent
      </h1>

      <p className="mt-4">
        Backend Status: {status}
      </p>
    </main>
  );
}