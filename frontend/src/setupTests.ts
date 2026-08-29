import { TextDecoder, TextEncoder } from "node:util";
import "@testing-library/jest-dom";

// jsdom's test environment doesn't provide these globals, but react-router-dom
// (via its dependency on the URL/streams APIs) expects them to exist.
Object.assign(global, { TextEncoder, TextDecoder });
