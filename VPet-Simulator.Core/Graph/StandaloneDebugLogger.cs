using System;
using System.IO;
using System.Text;

namespace VPet_Simulator.Core
{
    public static class StandaloneDebugLogger
    {
        private const string FileName = "standalone-cat-debug.log";
        private static readonly object WriteLock = new object();

        public static string LogFilePath { get; } = ResolveLogFilePath();

        private static string ResolveLogFilePath()
        {
            var primaryPath = Path.Combine(AppContext.BaseDirectory, FileName);
            try
            {
                File.AppendAllText(primaryPath, string.Empty);
                return primaryPath;
            }
            catch
            {
                var fallbackDirectory = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
                var fallbackPath = Path.Combine(fallbackDirectory, FileName);
                try
                {
                    Directory.CreateDirectory(fallbackDirectory);
                    File.AppendAllText(fallbackPath, string.Empty);
                }
                catch
                {
                }
                return fallbackPath;
            }
        }

        public static void Log(string message)
        {
            try
            {
                var timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff");
                var lines = (message ?? string.Empty).Replace("\r\n", "\n").Split('\n');
                var output = new StringBuilder();
                foreach (var line in lines)
                    output.Append('[').Append(timestamp).Append("][Thread:")
                        .Append(Environment.CurrentManagedThreadId).Append("] ").AppendLine(line);

                lock (WriteLock)
                    File.AppendAllText(LogFilePath, output.ToString());
            }
            catch
            {
            }
        }
    }
}
