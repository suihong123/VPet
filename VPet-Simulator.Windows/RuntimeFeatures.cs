namespace VPet_Simulator.Windows;

/// <summary>
/// Central feature switches for the standalone desktop pet runtime mode.
/// </summary>
public static class RuntimeFeatures
{
    public static bool StandaloneMode => true;

    public static bool EnableSteam => false;

    public static bool EnableWorkshop => false;

    public static bool EnableNetwork => false;

    public static bool EnableMultiplayer => false;

    public static bool EnableTelemetry => false;

    public static bool EnablePluginDll => true;

    public static bool EnableLocalMods => true;

    public static string DefaultPetId => "vup";
}
