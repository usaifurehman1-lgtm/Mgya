package com.mygame.app;

import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.unity3d.ads.UnityAds;

@CapacitorPlugin(name = "UnityAds")
public class UnityAdsPlugin extends Plugin {

    @com.getcapacitor.PluginMethod
    public void initialize(PluginCall call) {
        String gameId = call.getString("gameId", "800386783");

        UnityAds.initialize(getActivity(), gameId, false,
            new UnityAds.IUnityAdsInitializationListener() {
                @Override
                public void onInitializationComplete() {
                    call.resolve();
                }

                @Override
                public void onInitializationFailed(
                    UnityAds.UnityAdsInitializationError error,
                    String message) {
                    call.reject(message);
                }
            });
    }

    @com.getcapacitor.PluginMethod
    public void showRewarded(PluginCall call) {
        String placementId = call.getString("placementId", "18968513796763");

        UnityAds.show(getActivity(), placementId,
            new UnityAds.IUnityAdsShowListener() {
                @Override
                public void onUnityAdsShowFailure(
                    String placementId,
                    UnityAds.UnityAdsShowError error,
                    String message) {
                    call.reject(message);
                }

                @Override
                public void onUnityAdsShowStart(String placementId) {}

                @Override
                public void onUnityAdsShowClick(String placementId) {}

                @Override
                public void onUnityAdsShowComplete(
                    String placementId,
                    UnityAds.UnityAdsShowCompletionState state) {
                    if (state == UnityAds.UnityAdsShowCompletionState.COMPLETED) {
                        call.resolve();
                    } else {
                        call.reject("Reward not completed");
                    }
                }
            });
    }
}
