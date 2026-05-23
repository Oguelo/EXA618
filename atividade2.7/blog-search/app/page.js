"use client";

import React, { useState, useEffect } from "react";

function SearchBar({ filterText, onFilterTextChange }) {
  return (
    <form style={{ marginBottom: "30px" }}>
      <label
        style={{ display: "block", marginBottom: "5px", fontSize: "16px" }}
      >
        Procure uma mensagem:
      </label>
      <input
        type="text"
        value={filterText}
        placeholder="Search..."
        onChange={(e) => onFilterTextChange(e.target.value)}
        style={{
          width: "100%",
          maxWidth: "600px",
          padding: "8px",
          backgroundColor: "#222",
          color: "white",
          border: "1px solid #444",
          borderRadius: "4px",
        }}
      />
    </form>
  );
}

function MessageRow({ message }) {
  const msgText = message[0] || "";
  const author = message[1] || "";
  const rawDate = message[2] || "";

  let formatarData = rawDate;
  if (rawDate) {
    try {
      const d = new Date(rawDate);
      formatarData = d.toLocaleString("pt-BR");
    } catch (e) {
      console.error("Erro ao formatar data", e);
    }
  }

  return (
    <tr style={{ borderBottom: "1px solid #333" }}>
      <td style={{ padding: "10px", width: "25%" }}>{author}</td>
      <td style={{ padding: "10px", width: "50%" }}>{msgText}</td>
      <td style={{ padding: "10px", width: "25%" }}>{formatarData}</td>
    </tr>
  );
}

function ListaMensagens({ messages, filterText }) {
  const rows = [];

  messages.forEach((msg, index) => {
    const searchString = msg.join(" ").toLowerCase();

    if (searchString.indexOf(filterText.toLowerCase()) === -1) {
      return;
    }

    rows.push(<MessageRow message={msg} key={index} />);
  });

  return (
    <table
      style={{
        width: "100%",
        maxWidth: "800px",
        borderCollapse: "collapse",
        textAlign: "left",
      }}
    >
      <thead>
        <tr>
          <th style={{ padding: "10px", fontSize: "18px" }}>Author</th>
          <th style={{ padding: "10px", fontSize: "18px" }}>Message</th>
          <th style={{ padding: "10px", fontSize: "18px" }}>Date</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
}

function FiltrarLista({ messages }) {
  const [filterText, setFilterText] = useState("");

  return (
    <div
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <div style={{ width: "100%", maxWidth: "800px" }}>
        <SearchBar filterText={filterText} onFilterTextChange={setFilterText} />
        <ListaMensagens messages={messages} filterText={filterText} />
      </div>
    </div>
  );
}

export default function Home() {
  const [blogMessages, setBlogMessages] = useState([]);

  useEffect(() => {
    fetch(
      "https://script.google.com/macros/s/AKfycbzBn3sALe1rYjz7Ze-Ik7q9TEVP0I2V3XX7GNcecWP8NvCzGt4yO_RT1OlQp09TE9cU/exec",
    )
      .then((response) => response.json())
      .then((data) => {
        const messageArray = Array.isArray(data)
          ? data
          : data.messages || data.data || [data];
        setBlogMessages(messageArray);
      })
      .catch((error) => {
        console.error("Erro ao buscar as mensagens:", error);
      });
  }, []);

  return (
    <main
      style={{
        minHeight: "100vh",
        padding: "40px 20px",
        fontFamily: "sans-serif",
        color: "white",
      }}
    >
      <FiltrarLista messages={blogMessages} />
    </main>
  );
}
