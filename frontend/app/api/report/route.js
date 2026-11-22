const backendUrl = process.env.INTERNAL_API_URL || "http://127.0.0.1:8000";

export async function POST(request) {
  try {
    const response = await fetch(`${backendUrl}/report`, {
      method: "POST",
      body: await request.formData(),
      cache: "no-store"
    });

    return new Response(await response.arrayBuffer(), {
      status: response.status,
      headers: {
        "Content-Type": response.headers.get("Content-Type") || "application/json"
      }
    });
  } catch {
    return Response.json(
      { detail: "The analysis service is unavailable. Start the backend and try again." },
      { status: 503 }
    );
  }
}
